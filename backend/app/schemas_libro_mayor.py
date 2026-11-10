"""Esquemas de la API del Libro Mayor (CUU-006). Saldo positivo: deudor; negativo: acreedor."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class MovimientoMayorOut(BaseModel):
    fecha: date | None
    id_asiento: int
    numero_asiento: int | None
    tipo_origen: str | None
    estado: str | None
    concepto: str | None
    referencia: str | None
    id_venta: int | None
    id_compra: int | None
    debe: Decimal
    haber: Decimal
    saldo: Decimal


class CuentaMayorOut(BaseModel):
    id_cuenta: int
    codigo: str | None
    nombre: str | None
    tipo_cuenta: str | None
    naturaleza: str | None
    activa: bool
    saldo_inicial: Decimal
    total_debe: Decimal
    total_haber: Decimal
    saldo_final: Decimal
    movimientos: list[MovimientoMayorOut]


class LibroMayorOut(BaseModel):
    id_cuenta: int
    codigo: str | None
    nombre: str | None
    # False: la cuenta consultada es un rubro y el resultado reúne sus cuentas imputables.
    imputable: bool
    desde: date | None
    hasta: date | None
    cuentas: list[CuentaMayorOut]
    saldo_inicial: Decimal
    total_debe: Decimal
    total_haber: Decimal
    saldo_final: Decimal
