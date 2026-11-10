"""Motor de asientos: CUU-003 Gestionar Libro Diario y CUU-004 Registrar asiento manual.

También lo usarán los asientos automáticos de ventas y compras (CUU-001 / CUU-002).

Reglas (alcance 2.5 y CLAUDE.md):
- Partida doble: un asiento solo se contabiliza si el total del Debe es igual al del Haber.
- Cada línea imputa a una cuenta vigente e imputable, con un importe positivo en el Debe o en el Haber
  (no en ambos). Un asiento tiene al menos dos líneas.
- Estados: BORRADOR (pendiente, sin número ni efecto contable), ASENTADO (vigente) y ANULADO.
- Numeración correlativa al contabilizar; los borradores no tienen número.
- Nunca se borran ni se sobrescriben asientos ni líneas:
  - anular un asiento asentado genera un contra-asiento (REVERSION) con Debe y Haber invertidos, y el
    original queda ANULADO; anular un borrador solo lo marca ANULADO;
  - modificar un asiento asentado lo revierte y crea uno nuevo con los datos corregidos; modificar un
    borrador lo descarta (ANULADO) y crea uno nuevo.
- Los asientos de ventas y compras se gestionan desde su comprobante, no desde el Libro Diario.
- Efecto contable: cuentan los asientos ASENTADO y ANULADO que fueron contabilizados (con número);
  un anulado se compensa con su contra-asiento.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import auditoria
from app.errors import ErrorNegocio
from app.models import AsientoContable, DetalleAsiento, EstadoAsiento, OrigenAsiento, PlanCuenta, Usuario
from app.schemas_asientos import AsientoIn, LineaIn

TABLA = "ASIENTO_CONTABLE"
CERO = Decimal("0.00")


@dataclass
class Totales:
    debe: Decimal
    haber: Decimal

    @property
    def diferencia(self) -> Decimal:
        return self.debe - self.haber

    @property
    def balanceado(self) -> bool:
        return self.debe == self.haber and self.debe > 0


# ---------- Consulta (CUU-003 pasos 1-3) ----------


def listar(
    db: Session,
    desde: date | None,
    hasta: date | None,
    id_cuenta: int | None,
    tipo_origen: OrigenAsiento | None,
    estado: EstadoAsiento | None,
    limite: int = 500,
) -> list[AsientoContable]:
    consulta = select(AsientoContable)
    if desde:
        consulta = consulta.where(AsientoContable.fecha >= desde)
    if hasta:
        consulta = consulta.where(AsientoContable.fecha <= hasta)
    if id_cuenta:
        con_cuenta = select(DetalleAsiento.id_asiento).where(DetalleAsiento.id_cuenta == id_cuenta)
        consulta = consulta.where(AsientoContable.id_asiento.in_(con_cuenta))
    if tipo_origen:
        consulta = consulta.where(AsientoContable.tipo_origen == tipo_origen)
    if estado:
        consulta = consulta.where(AsientoContable.estado == estado)
    consulta = consulta.order_by(
        AsientoContable.fecha.desc(), AsientoContable.numero_asiento.desc(), AsientoContable.id_asiento.desc()
    ).limit(limite)
    return list(db.scalars(consulta))


def obtener(db: Session, id_asiento: int) -> AsientoContable:
    asiento = db.get(AsientoContable, id_asiento)
    if asiento is None:
        raise ErrorNegocio(404, "El asiento no existe.")
    return asiento


def lineas_de(db: Session, ids_asiento: list[int]) -> dict[int, list[tuple[DetalleAsiento, PlanCuenta]]]:
    """Líneas de varios asientos en una sola consulta, con su cuenta."""
    resultado: dict[int, list[tuple[DetalleAsiento, PlanCuenta]]] = {i: [] for i in ids_asiento}
    if not ids_asiento:
        return resultado
    consulta = (
        select(DetalleAsiento, PlanCuenta)
        .join(PlanCuenta, PlanCuenta.id_cuenta == DetalleAsiento.id_cuenta)
        .where(DetalleAsiento.id_asiento.in_(ids_asiento))
        .order_by(DetalleAsiento.id_asiento, DetalleAsiento.id_detalle_asiento)
    )
    for detalle, cuenta in db.execute(consulta):
        resultado[detalle.id_asiento].append((detalle, cuenta))
    return resultado


def contra_asientos_de(db: Session, ids_asiento: list[int]) -> dict[int, AsientoContable]:
    """Para cada asiento revertido, el contra-asiento que lo anuló."""
    if not ids_asiento:
        return {}
    consulta = select(AsientoContable).where(AsientoContable.id_asiento_revertido.in_(ids_asiento))
    return {c.id_asiento_revertido: c for c in db.scalars(consulta) if c.id_asiento_revertido is not None}


def calcular_totales(lineas: list[LineaIn]) -> Totales:
    return Totales(debe=sum((linea.debe for linea in lineas), CERO), haber=sum((linea.haber for linea in lineas), CERO))


# ---------- Validación (CUU-004 pasos 2-3) ----------


def validar_lineas(db: Session, lineas: list[LineaIn]) -> Totales:
    """Paso 2 / 2.a: cuentas vigentes e imputables e importes válidos. No exige balance."""
    if len(lineas) < 2:
        raise ErrorNegocio(422, "El asiento debe tener al menos dos líneas.")
    for numero, linea in enumerate(lineas, start=1):
        if (linea.debe > 0) == (linea.haber > 0):
            raise ErrorNegocio(
                422, f"Línea {numero}: indique un importe mayor a cero en el Debe o en el Haber, no en ambos."
            )
        cuenta = db.get(PlanCuenta, linea.id_cuenta)
        if cuenta is None:
            raise ErrorNegocio(422, f"Línea {numero}: la cuenta no existe.")
        if not cuenta.esta_activa:
            raise ErrorNegocio(422, f"Línea {numero}: la cuenta {cuenta.codigo} está dada de baja.")
        if not cuenta.es_imputable:
            raise ErrorNegocio(422, f"Línea {numero}: la cuenta {cuenta.codigo} es un rubro y no recibe imputaciones.")
    return calcular_totales(lineas)


def verificar_balance(totales: Totales) -> None:
    """Paso 3 / 3.a: partida doble."""
    if not totales.balanceado:
        raise ErrorNegocio(
            422,
            f"El asiento no está balanceado: Debe {totales.debe:.2f}, Haber {totales.haber:.2f}, "
            f"diferencia {abs(totales.diferencia):.2f}.",
        )


# ---------- Alta y confirmación (CUU-004) ----------


def crear(
    db: Session,
    datos: AsientoIn,
    actor: Usuario,
    origen: str | None,
    tipo_origen: OrigenAsiento = OrigenAsiento.MANUAL,
    id_venta: int | None = None,
    id_compra: int | None = None,
) -> AsientoContable:
    """Registra el asiento como borrador o, si datos.confirmar, lo contabiliza (pasos 4-5)."""
    asiento = _registrar(db, datos, tipo_origen, id_venta=id_venta, id_compra=id_compra)
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=asiento.id_asiento,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(db, asiento),
    )
    _confirmar_transaccion(db)
    return asiento


def confirmar(db: Session, id_asiento: int, actor: Usuario, origen: str | None) -> AsientoContable:
    """Contabiliza un borrador: valida de nuevo cuentas y balance, y le asigna número."""
    asiento = obtener(db, id_asiento)
    if asiento.estado != EstadoAsiento.BORRADOR:
        raise ErrorNegocio(409, "Solo se pueden confirmar asientos en borrador.")
    lineas = [
        LineaIn(id_cuenta=d.id_cuenta, debe=d.debe or CERO, haber=d.haber or CERO)
        for d, _ in lineas_de(db, [id_asiento])[id_asiento]
    ]
    verificar_balance(validar_lineas(db, lineas))
    antes = _instantanea(db, asiento)
    asiento.estado = EstadoAsiento.ASENTADO
    asiento.numero_asiento = _proximo_numero(db)
    auditoria.registrar(
        db,
        accion="CONFIRMACION",
        tabla=TABLA,
        id_registro=asiento.id_asiento,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(db, asiento),
    )
    _confirmar_transaccion(db)
    return asiento


# ---------- Anulación y modificación (CUU-003 3.a / 3.b) ----------


def anular(db: Session, id_asiento: int, actor: Usuario, origen: str | None) -> AsientoContable:
    """3.b: un borrador se descarta; un asiento asentado se revierte con un contra-asiento.
    Devuelve el contra-asiento, o el borrador descartado."""
    asiento = _modificable(db, id_asiento)
    resultado = _anular_sin_confirmar(db, asiento, actor, origen)
    _confirmar_transaccion(db)
    return resultado


def modificar(db: Session, id_asiento: int, datos: AsientoIn, actor: Usuario, origen: str | None) -> AsientoContable:
    """3.a: el asiento original no se edita. Se anula (con contra-asiento si estaba asentado) y se registra
    uno nuevo con los datos corregidos. Devuelve el asiento nuevo."""
    asiento = _modificable(db, id_asiento)
    estaba_asentado = asiento.estado == EstadoAsiento.ASENTADO
    if estaba_asentado:
        datos = datos.model_copy(update={"confirmar": True})  # un asiento vigente se reemplaza por otro vigente
    if not datos.referencia:
        datos = datos.model_copy(update={"referencia": f"Rectifica el asiento {_descripcion(asiento)}"})

    # Validar antes de anular, para no dejar el original anulado si los datos nuevos son inválidos.
    totales = validar_lineas(db, datos.lineas)
    if datos.confirmar:
        verificar_balance(totales)
    antes = _instantanea(db, asiento)
    _anular_sin_confirmar(db, asiento, actor, origen)
    nuevo = _registrar(db, datos, OrigenAsiento.MANUAL)
    auditoria.registrar(
        db,
        accion="MODIFICACION",
        tabla=TABLA,
        id_registro=nuevo.id_asiento,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(db, nuevo),
    )
    _confirmar_transaccion(db)
    return nuevo


# ---------- Auxiliares ----------


def _registrar(
    db: Session,
    datos: AsientoIn,
    tipo_origen: OrigenAsiento,
    id_venta: int | None = None,
    id_compra: int | None = None,
    id_asiento_revertido: int | None = None,
) -> AsientoContable:
    totales = validar_lineas(db, datos.lineas)
    if datos.confirmar:
        verificar_balance(totales)
    asiento = AsientoContable(
        fecha=datos.fecha,
        concepto=datos.concepto,
        referencia=datos.referencia or None,
        tipo_origen=tipo_origen,
        id_venta=id_venta,
        id_compra=id_compra,
        id_asiento_revertido=id_asiento_revertido,
        estado=EstadoAsiento.ASENTADO if datos.confirmar else EstadoAsiento.BORRADOR,
        numero_asiento=_proximo_numero(db) if datos.confirmar else None,
    )
    db.add(asiento)
    db.flush()
    for linea in datos.lineas:
        db.add(
            DetalleAsiento(id_asiento=asiento.id_asiento, id_cuenta=linea.id_cuenta, debe=linea.debe, haber=linea.haber)
        )
    db.flush()
    return asiento


def _modificable(db: Session, id_asiento: int) -> AsientoContable:
    asiento = obtener(db, id_asiento)
    if asiento.estado == EstadoAsiento.ANULADO:
        raise ErrorNegocio(409, "El asiento ya está anulado.")
    if asiento.tipo_origen == OrigenAsiento.REVERSION:
        raise ErrorNegocio(409, "Un contra-asiento no se modifica ni se anula.")
    if asiento.tipo_origen in (OrigenAsiento.VENTA, OrigenAsiento.COMPRA):
        raise ErrorNegocio(
            409,
            "Los asientos de ventas y compras se modifican o anulan desde su comprobante, no desde el Libro Diario.",
        )
    return asiento


def _anular_sin_confirmar(db: Session, asiento: AsientoContable, actor: Usuario, origen: str | None) -> AsientoContable:
    antes = _instantanea(db, asiento)
    if asiento.estado == EstadoAsiento.BORRADOR:
        asiento.estado = EstadoAsiento.ANULADO
        auditoria.registrar(
            db,
            accion="ANULACION",
            tabla=TABLA,
            id_registro=asiento.id_asiento,
            actor=actor.email,
            origen=origen,
            antes=antes,
            despues=_instantanea(db, asiento),
        )
        return asiento

    lineas_originales = lineas_de(db, [asiento.id_asiento])[asiento.id_asiento]
    contra = _registrar(
        db,
        AsientoIn(
            fecha=asiento.fecha or date.today(),
            concepto=f"Reversión del asiento {_descripcion(asiento)}: {asiento.concepto}"[:255],
            referencia=asiento.referencia,
            lineas=[
                LineaIn(id_cuenta=d.id_cuenta, debe=d.haber or CERO, haber=d.debe or CERO) for d, _ in lineas_originales
            ],
            confirmar=True,
        ),
        OrigenAsiento.REVERSION,
        id_asiento_revertido=asiento.id_asiento,
    )
    asiento.estado = EstadoAsiento.ANULADO
    auditoria.registrar(
        db,
        accion="REVERSION",
        tabla=TABLA,
        id_registro=asiento.id_asiento,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues={**_instantanea(db, asiento), "contra_asiento": contra.numero_asiento},
    )
    return contra


def _proximo_numero(db: Session) -> int:
    return (db.scalar(select(func.max(AsientoContable.numero_asiento))) or 0) + 1


def _descripcion(asiento: AsientoContable) -> str:
    return f"N° {asiento.numero_asiento}" if asiento.numero_asiento else f"borrador {asiento.id_asiento}"


def _instantanea(db: Session, asiento: AsientoContable) -> dict[str, Any]:
    lineas = lineas_de(db, [asiento.id_asiento])[asiento.id_asiento]
    return {
        "numero_asiento": asiento.numero_asiento,
        "fecha": asiento.fecha,
        "concepto": asiento.concepto,
        "referencia": asiento.referencia,
        "tipo_origen": asiento.tipo_origen,
        "estado": asiento.estado,
        "lineas": [{"cuenta": c.codigo, "debe": str(d.debe), "haber": str(d.haber)} for d, c in lineas],
    }


def _confirmar_transaccion(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:  # dos asientos confirmados a la vez con el mismo número
        db.rollback()
        raise ErrorNegocio(409, "Otro usuario contabilizó un asiento al mismo tiempo. Intente nuevamente.") from exc
