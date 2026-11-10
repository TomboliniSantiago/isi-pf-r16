"""CUU-006 Consultar Libro Mayor.

El Libro Mayor no se guarda: se calcula desde los asientos, que son la única fuente de verdad. Así nunca
queda desactualizado respecto del Libro Diario (la tabla LIBRO_MAYOR del esquema base no se usa).

- Movimientos: líneas de los asientos contabilizados (con número), de cualquier origen (ventas, compras,
  asientos manuales, modificaciones y anulaciones). Un asiento anulado sigue apareciendo junto a su
  contra-asiento, que lo compensa. Los borradores (pendientes) no tienen efecto contable.
- Paso 1: se consulta una cuenta imputable o un rubro; un rubro reúne sus cuentas imputables descendientes.
- Paso 2: saldo inicial = Debe − Haber acumulado antes del período; luego el Debe y el Haber del período,
  el saldo después de cada movimiento y el saldo final. Saldo positivo: deudor; negativo: acreedor.
- 2.a: sin movimientos en el período se informa el saldo inicial arrastrado.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.errors import ErrorNegocio
from app.models import AsientoContable, DetalleAsiento, PlanCuenta

CERO = Decimal("0.00")


@dataclass
class Movimiento:
    detalle: DetalleAsiento
    asiento: AsientoContable
    saldo: Decimal


@dataclass
class MayorCuenta:
    cuenta: PlanCuenta
    saldo_inicial: Decimal
    movimientos: list[Movimiento] = field(default_factory=list)

    @property
    def total_debe(self) -> Decimal:
        return sum((m.detalle.debe or CERO for m in self.movimientos), CERO)

    @property
    def total_haber(self) -> Decimal:
        return sum((m.detalle.haber or CERO for m in self.movimientos), CERO)

    @property
    def saldo_final(self) -> Decimal:
        return self.saldo_inicial + self.total_debe - self.total_haber


def consultar(
    db: Session, id_cuenta: int, desde: date | None, hasta: date | None
) -> tuple[PlanCuenta, list[MayorCuenta]]:
    if desde and hasta and desde > hasta:
        raise ErrorNegocio(422, "La fecha desde no puede ser posterior a la fecha hasta.")
    consultada = db.get(PlanCuenta, id_cuenta)
    if consultada is None:
        raise ErrorNegocio(404, "La cuenta no existe.")
    cuentas = [consultada] if consultada.es_imputable else _imputables_de(db, consultada)
    if not cuentas:
        return consultada, []
    ids = [c.id_cuenta for c in cuentas]
    contabilizado = AsientoContable.numero_asiento.is_not(None)

    iniciales: dict[int, Decimal] = defaultdict(lambda: CERO)
    if desde:
        consulta = (
            select(DetalleAsiento.id_cuenta, func.sum(DetalleAsiento.debe), func.sum(DetalleAsiento.haber))
            .join(AsientoContable, AsientoContable.id_asiento == DetalleAsiento.id_asiento)
            .where(DetalleAsiento.id_cuenta.in_(ids), contabilizado, AsientoContable.fecha < desde)
            .group_by(DetalleAsiento.id_cuenta)
        )
        for id_c, debe, haber in db.execute(consulta):
            iniciales[id_c] = Decimal(debe or 0) - Decimal(haber or 0)

    mayores = {c.id_cuenta: MayorCuenta(cuenta=c, saldo_inicial=iniciales[c.id_cuenta]) for c in cuentas}
    consulta = (
        select(DetalleAsiento, AsientoContable)
        .join(AsientoContable, AsientoContable.id_asiento == DetalleAsiento.id_asiento)
        .where(DetalleAsiento.id_cuenta.in_(ids), contabilizado)
        .order_by(AsientoContable.fecha, AsientoContable.numero_asiento, DetalleAsiento.id_detalle_asiento)
    )
    if desde:
        consulta = consulta.where(AsientoContable.fecha >= desde)
    if hasta:
        consulta = consulta.where(AsientoContable.fecha <= hasta)
    saldos = {id_c: m.saldo_inicial for id_c, m in mayores.items()}
    for detalle, asiento in db.execute(consulta):
        saldos[detalle.id_cuenta] += (detalle.debe or CERO) - (detalle.haber or CERO)
        mayores[detalle.id_cuenta].movimientos.append(Movimiento(detalle, asiento, saldos[detalle.id_cuenta]))

    resultado = list(mayores.values())
    if not consultada.es_imputable:
        # En un rubro se omiten las cuentas sin saldo ni movimientos en el período.
        resultado = [m for m in resultado if m.movimientos or m.saldo_inicial]
    return consultada, sorted(resultado, key=lambda m: _orden(m.cuenta.codigo))


def _imputables_de(db: Session, rubro: PlanCuenta) -> list[PlanCuenta]:
    """Cuentas imputables descendientes del rubro (activas o dadas de baja: pueden tener historia)."""
    hijas: dict[int | None, list[PlanCuenta]] = defaultdict(list)
    for c in db.scalars(select(PlanCuenta)):
        hijas[c.id_cuenta_padre].append(c)
    resultado, pendientes, vistas = [], [rubro.id_cuenta], set()
    while pendientes:
        actual = pendientes.pop()
        if actual in vistas:  # protección ante ciclos en datos heredados
            continue
        vistas.add(actual)
        for hija in hijas.get(actual, []):
            if hija.es_imputable:
                resultado.append(hija)
            else:
                pendientes.append(hija.id_cuenta)
    return resultado


def _orden(codigo: str | None) -> tuple[int, ...]:
    return tuple(int(p) for p in (codigo or "").split(".") if p.isdigit())
