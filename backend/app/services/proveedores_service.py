"""CUU-008 Gestionar Proveedores (alta, modificación, consulta y baja lógica).

- Alta (pasos 3-6): el CUIT se valida (formato y dígito verificador) y se consulta en el padrón de ARCA
  para completar los datos; no puede haber dos proveedores con el mismo CUIT, activos o dados de baja (4.a).
  El código del proveedor (PRV-000001) se deriva de su id.
- Modificación (2.a): el CUIT solo puede cambiarse si el proveedor no tiene comprobantes asociados.
- Baja lógica (2.b): no se permite si el proveedor tiene comprobantes pendientes de procesamiento, es decir,
  compras cuyo asiento no está asentado. A diferencia de las ventas, COMPRA no registra CAE.
"""

from typing import Any

from sqlalchemy import case, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import auditoria
from app.arca.padron import DatosPadron, Padron
from app.cuit import normalizar_cuit
from app.errors import ErrorNegocio
from app.models import (
    CUENTA_NO,
    CUENTA_SI,
    ESTADO_ASIENTO_ASENTADO,
    AsientoContable,
    Compra,
    CondicionIva,
    EstadoCompra,
    Proveedor,
    Usuario,
)
from app.schemas_proveedores import ProveedorIn

TABLA = "PROVEEDOR"


# ---------- Consulta (paso 1 y 2.c) ----------


def listar(db: Session, buscar: str | None, condicion_iva: CondicionIva | None, activo: bool | None) -> list[Proveedor]:
    consulta = select(Proveedor).order_by(Proveedor.razon_social)
    if buscar and buscar.strip():
        texto = buscar.strip()
        digitos = "".join(c for c in texto if c.isdigit())
        filtros = [Proveedor.razon_social.ilike(f"%{texto}%")]
        if digitos:  # el CUIT se busca sin importar los guiones
            filtros.append(func.replace(Proveedor.cuit, "-", "").like(f"%{digitos}%"))
        consulta = consulta.where(or_(*filtros))
    if condicion_iva is not None:
        consulta = consulta.where(Proveedor.condicion_iva == condicion_iva)
    if activo is True:
        consulta = consulta.where(Proveedor.activo == CUENTA_SI)
    elif activo is False:
        consulta = consulta.where(or_(Proveedor.activo != CUENTA_SI, Proveedor.activo.is_(None)))
    return list(db.scalars(consulta))


def obtener(db: Session, id_proveedor: int) -> Proveedor:
    proveedor = db.get(Proveedor, id_proveedor)
    if proveedor is None:
        raise ErrorNegocio(404, "El proveedor no existe.")
    return proveedor


def comprobantes(db: Session, id_proveedor: int) -> list[tuple[Compra, bool]]:
    """Compras del proveedor, de la más reciente a la más antigua, con la marca de si están asentadas."""
    hay_asiento = (
        select(AsientoContable.id_asiento)
        .where(AsientoContable.id_compra == Compra.id_compra, AsientoContable.estado == ESTADO_ASIENTO_ASENTADO)
        .exists()
    )
    # SQL Server no admite EXISTS como columna del SELECT: se envuelve en CASE.
    asentada = case((hay_asiento, 1), else_=0)
    consulta = (
        select(Compra, asentada)
        .where(Compra.id_proveedor == id_proveedor)
        .order_by(Compra.fecha_emision.desc(), Compra.id_compra.desc())
    )
    return [(compra, bool(es_asentada)) for compra, es_asentada in db.execute(consulta)]


def es_pendiente(compra: Compra, asentada: bool) -> bool:
    """Pendiente de procesamiento: la compra todavía no tiene su asiento asentado. Una anulada no lo está."""
    if compra.estado == EstadoCompra.ANULADA:
        return False
    return not asentada


def consultar_cuit(db: Session, cuit: str, padron: Padron) -> tuple[str, DatosPadron | None, Proveedor | None]:
    """Pasos 3-4: normaliza el CUIT, lo busca en el padrón y en los proveedores ya registrados."""
    cuit = normalizar_cuit(cuit)
    existente = db.scalar(select(Proveedor).where(Proveedor.cuit == cuit))
    return cuit, padron.consultar(cuit), existente


# ---------- Alta y modificación (pasos 2-6 y 2.a) ----------


def crear(db: Session, datos: ProveedorIn, actor: Usuario, origen: str | None) -> Proveedor:
    cuit = normalizar_cuit(datos.cuit)
    _verificar_cuit_libre(db, cuit)
    proveedor = Proveedor(activo=CUENTA_SI)
    _aplicar(proveedor, datos, cuit)
    db.add(proveedor)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=proveedor.id_proveedor,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(proveedor),
    )
    _confirmar(db)
    return proveedor


def modificar(db: Session, id_proveedor: int, datos: ProveedorIn, actor: Usuario, origen: str | None) -> Proveedor:
    proveedor = obtener(db, id_proveedor)
    cuit = normalizar_cuit(datos.cuit)
    if cuit != proveedor.cuit:
        _verificar_cuit_libre(db, cuit, excluir=proveedor.id_proveedor)
        if comprobantes(db, id_proveedor):
            raise ErrorNegocio(409, "El proveedor tiene comprobantes asociados: no se puede cambiar su CUIT.")
    antes = _instantanea(proveedor)
    _aplicar(proveedor, datos, cuit)
    despues = _instantanea(proveedor)
    if antes != despues:
        auditoria.registrar(
            db,
            accion="MODIFICACION",
            tabla=TABLA,
            id_registro=proveedor.id_proveedor,
            actor=actor.email,
            origen=origen,
            antes=antes,
            despues=despues,
        )
    _confirmar(db)
    return proveedor


# ---------- Baja lógica (2.b) y reactivación ----------


def verificar_baja(db: Session, id_proveedor: int) -> Proveedor:
    """2.b.2: el proveedor no debe tener comprobantes pendientes de procesamiento."""
    proveedor = obtener(db, id_proveedor)
    if not proveedor.esta_activo:
        raise ErrorNegocio(409, "El proveedor ya se encuentra dado de baja.")
    pendientes = [c for c, asentada in comprobantes(db, id_proveedor) if es_pendiente(c, asentada)]
    if pendientes:
        raise ErrorNegocio(
            409,
            f"El proveedor tiene {len(pendientes)} comprobante(s) pendiente(s) de procesamiento "
            "(sin asiento asentado): no puede darse de baja.",
        )
    return proveedor


def dar_de_baja(db: Session, id_proveedor: int, actor: Usuario, origen: str | None) -> Proveedor:
    proveedor = verificar_baja(db, id_proveedor)
    antes = _instantanea(proveedor)
    proveedor.activo = CUENTA_NO
    auditoria.registrar(
        db,
        accion="BAJA",
        tabla=TABLA,
        id_registro=proveedor.id_proveedor,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(proveedor),
    )
    _confirmar(db)
    return proveedor


def reactivar(db: Session, id_proveedor: int, actor: Usuario, origen: str | None) -> Proveedor:
    proveedor = obtener(db, id_proveedor)
    if proveedor.esta_activo:
        raise ErrorNegocio(409, "El proveedor ya se encuentra activo.")
    antes = _instantanea(proveedor)
    proveedor.activo = CUENTA_SI
    auditoria.registrar(
        db,
        accion="REACTIVACION",
        tabla=TABLA,
        id_registro=proveedor.id_proveedor,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(proveedor),
    )
    _confirmar(db)
    return proveedor


# ---------- Auxiliares ----------


def _verificar_cuit_libre(db: Session, cuit: str, excluir: int | None = None) -> None:
    """4.a: informa el proveedor que ya tiene el CUIT, para que el usuario lo use o lo reactive."""
    existente = db.scalar(select(Proveedor).where(Proveedor.cuit == cuit))
    if existente is not None and existente.id_proveedor != excluir:
        estado = "" if existente.esta_activo else ", dado de baja"
        raise ErrorNegocio(
            409, f"Ya existe un proveedor con el CUIT {cuit}: {existente.razon_social} ({existente.codigo}{estado})."
        )


def _aplicar(proveedor: Proveedor, datos: ProveedorIn, cuit: str) -> None:
    proveedor.cuit = cuit
    proveedor.razon_social = datos.razon_social
    proveedor.condicion_iva = datos.condicion_iva
    proveedor.domicilio = datos.domicilio
    proveedor.localidad = datos.localidad or None
    proveedor.provincia = datos.provincia or None


def _instantanea(proveedor: Proveedor) -> dict[str, Any]:
    return {
        "cuit": proveedor.cuit,
        "razon_social": proveedor.razon_social,
        "condicion_iva": proveedor.condicion_iva,
        "domicilio": proveedor.domicilio,
        "localidad": proveedor.localidad,
        "provincia": proveedor.provincia,
        "activo": proveedor.activo,
    }


def _confirmar(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:  # carrera contra el índice único de CUIT
        db.rollback()
        raise ErrorNegocio(409, "Ya existe un proveedor con ese CUIT.") from exc
