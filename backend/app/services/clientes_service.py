"""CUU-007 Gestionar Clientes (alta, modificación, consulta y baja lógica).

- Alta (pasos 3-6): el CUIT se valida (formato y dígito verificador) y se consulta en el padrón de ARCA
  para completar los datos; no puede haber dos clientes con el mismo CUIT, activos o dados de baja (4.a).
  El código del cliente (CLI-000001) se deriva de su id.
- Modificación (2.a): el CUIT solo puede cambiarse si el cliente no tiene comprobantes asociados.
- Baja lógica (2.c): no se permite si el cliente tiene comprobantes pendientes de procesamiento, es decir,
  ventas sin CAE (no validadas con ARCA) o cuyo asiento no está asentado.
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
    Cliente,
    CondicionIva,
    EstadoVenta,
    Usuario,
    Venta,
)
from app.schemas_clientes import ClienteIn

TABLA = "CLIENTE"


# ---------- Consulta (paso 1 y 2.b) ----------


def listar(db: Session, buscar: str | None, condicion_iva: CondicionIva | None, activo: bool | None) -> list[Cliente]:
    consulta = select(Cliente).order_by(Cliente.razon_social)
    if buscar and buscar.strip():
        texto = buscar.strip()
        digitos = "".join(c for c in texto if c.isdigit())
        filtros = [Cliente.razon_social.ilike(f"%{texto}%")]
        if digitos:  # el CUIT se busca sin importar los guiones
            filtros.append(func.replace(Cliente.cuit, "-", "").like(f"%{digitos}%"))
        consulta = consulta.where(or_(*filtros))
    if condicion_iva is not None:
        consulta = consulta.where(Cliente.condicion_iva == condicion_iva)
    if activo is True:
        consulta = consulta.where(Cliente.activo == CUENTA_SI)
    elif activo is False:
        consulta = consulta.where(or_(Cliente.activo != CUENTA_SI, Cliente.activo.is_(None)))
    return list(db.scalars(consulta))


def obtener(db: Session, id_cliente: int) -> Cliente:
    cliente = db.get(Cliente, id_cliente)
    if cliente is None:
        raise ErrorNegocio(404, "El cliente no existe.")
    return cliente


def comprobantes(db: Session, id_cliente: int) -> list[tuple[Venta, bool]]:
    """Ventas del cliente, de la más reciente a la más antigua, con la marca de si están asentadas."""
    hay_asiento = (
        select(AsientoContable.id_asiento)
        .where(AsientoContable.id_venta == Venta.id_venta, AsientoContable.estado == ESTADO_ASIENTO_ASENTADO)
        .exists()
    )
    # SQL Server no admite EXISTS como columna del SELECT: se envuelve en CASE.
    asentada = case((hay_asiento, 1), else_=0)
    consulta = (
        select(Venta, asentada)
        .where(Venta.id_cliente == id_cliente)
        .order_by(Venta.fecha_emision.desc(), Venta.id_venta.desc())
    )
    return [(venta, bool(es_asentada)) for venta, es_asentada in db.execute(consulta)]


def es_pendiente(venta: Venta, asentada: bool) -> bool:
    """Pendiente de procesamiento: sin CAE (no validada con ARCA) o sin asiento asentado.
    Una venta anulada ya no está pendiente."""
    if venta.estado == EstadoVenta.ANULADA:
        return False
    return not venta.cae or not asentada


def consultar_cuit(db: Session, cuit: str, padron: Padron) -> tuple[str, DatosPadron | None, Cliente | None]:
    """Pasos 3-4: normaliza el CUIT, lo busca en el padrón y en los clientes ya registrados."""
    cuit = normalizar_cuit(cuit)
    existente = db.scalar(select(Cliente).where(Cliente.cuit == cuit))
    return cuit, padron.consultar(cuit), existente


# ---------- Alta y modificación (pasos 2-6 y 2.a) ----------


def crear(db: Session, datos: ClienteIn, actor: Usuario, origen: str | None) -> Cliente:
    cuit = normalizar_cuit(datos.cuit)
    _verificar_cuit_libre(db, cuit)
    cliente = Cliente(activo=CUENTA_SI)
    _aplicar(cliente, datos, cuit)
    db.add(cliente)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=cliente.id_cliente,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(cliente),
    )
    _confirmar(db)
    return cliente


def modificar(db: Session, id_cliente: int, datos: ClienteIn, actor: Usuario, origen: str | None) -> Cliente:
    cliente = obtener(db, id_cliente)
    cuit = normalizar_cuit(datos.cuit)
    if cuit != cliente.cuit:
        _verificar_cuit_libre(db, cuit, excluir=cliente.id_cliente)
        if comprobantes(db, id_cliente):
            raise ErrorNegocio(409, "El cliente tiene comprobantes asociados: no se puede cambiar su CUIT.")
    antes = _instantanea(cliente)
    _aplicar(cliente, datos, cuit)
    despues = _instantanea(cliente)
    if antes != despues:
        auditoria.registrar(
            db,
            accion="MODIFICACION",
            tabla=TABLA,
            id_registro=cliente.id_cliente,
            actor=actor.email,
            origen=origen,
            antes=antes,
            despues=despues,
        )
    _confirmar(db)
    return cliente


# ---------- Baja lógica (2.c) y reactivación ----------


def verificar_baja(db: Session, id_cliente: int) -> Cliente:
    """2.c.2: el cliente no debe tener comprobantes pendientes de procesamiento."""
    cliente = obtener(db, id_cliente)
    if not cliente.esta_activo:
        raise ErrorNegocio(409, "El cliente ya se encuentra dado de baja.")
    pendientes = [v for v, asentada in comprobantes(db, id_cliente) if es_pendiente(v, asentada)]
    if pendientes:
        raise ErrorNegocio(
            409,
            f"El cliente tiene {len(pendientes)} comprobante(s) pendiente(s) de procesamiento "
            "(sin CAE o sin asiento asentado): no puede darse de baja.",
        )
    return cliente


def dar_de_baja(db: Session, id_cliente: int, actor: Usuario, origen: str | None) -> Cliente:
    cliente = verificar_baja(db, id_cliente)
    antes = _instantanea(cliente)
    cliente.activo = CUENTA_NO
    auditoria.registrar(
        db,
        accion="BAJA",
        tabla=TABLA,
        id_registro=cliente.id_cliente,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(cliente),
    )
    _confirmar(db)
    return cliente


def reactivar(db: Session, id_cliente: int, actor: Usuario, origen: str | None) -> Cliente:
    cliente = obtener(db, id_cliente)
    if cliente.esta_activo:
        raise ErrorNegocio(409, "El cliente ya se encuentra activo.")
    antes = _instantanea(cliente)
    cliente.activo = CUENTA_SI
    auditoria.registrar(
        db,
        accion="REACTIVACION",
        tabla=TABLA,
        id_registro=cliente.id_cliente,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(cliente),
    )
    _confirmar(db)
    return cliente


# ---------- Auxiliares ----------


def _verificar_cuit_libre(db: Session, cuit: str, excluir: int | None = None) -> None:
    """4.a: informa el cliente que ya tiene el CUIT, para que el usuario lo use o lo reactive."""
    existente = db.scalar(select(Cliente).where(Cliente.cuit == cuit))
    if existente is not None and existente.id_cliente != excluir:
        estado = "" if existente.esta_activo else ", dado de baja"
        raise ErrorNegocio(
            409, f"Ya existe un cliente con el CUIT {cuit}: {existente.razon_social} ({existente.codigo}{estado})."
        )


def _aplicar(cliente: Cliente, datos: ClienteIn, cuit: str) -> None:
    cliente.cuit = cuit
    cliente.razon_social = datos.razon_social
    cliente.condicion_iva = datos.condicion_iva
    cliente.domicilio = datos.domicilio
    cliente.localidad = datos.localidad or None
    cliente.provincia = datos.provincia or None


def _instantanea(cliente: Cliente) -> dict[str, Any]:
    return {
        "cuit": cliente.cuit,
        "razon_social": cliente.razon_social,
        "condicion_iva": cliente.condicion_iva,
        "domicilio": cliente.domicilio,
        "localidad": cliente.localidad,
        "provincia": cliente.provincia,
        "activo": cliente.activo,
    }


def _confirmar(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:  # carrera contra el índice único de CUIT
        db.rollback()
        raise ErrorNegocio(409, "Ya existe un cliente con ese CUIT.") from exc
