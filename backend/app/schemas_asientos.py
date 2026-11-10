"""Esquemas de la API del Libro Diario y los asientos manuales (CUU-003 / CUU-004)."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

Importe = Annotated[Decimal, Field(ge=0, max_digits=15, decimal_places=2)]


class LineaIn(BaseModel):
    id_cuenta: int
    debe: Importe = Decimal("0")
    haber: Importe = Decimal("0")


class AsientoIn(BaseModel):
    fecha: date
    concepto: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
    referencia: Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)] | None = None
    lineas: list[LineaIn] = Field(min_length=2, max_length=100)
    # False: se guarda como borrador (pendiente); True: se contabiliza (CUU-004 paso 5).
    confirmar: bool = False


class LineaOut(BaseModel):
    id_detalle_asiento: int
    id_cuenta: int
    codigo: str | None
    nombre: str | None
    debe: Decimal
    haber: Decimal


class AsientoOut(BaseModel):
    id_asiento: int
    numero_asiento: int | None
    fecha: date | None
    concepto: str | None
    referencia: str | None
    tipo_origen: str | None
    estado: str | None
    id_venta: int | None
    id_compra: int | None
    # Contra-asientos: el asiento que revierte y, en el revertido, el contra-asiento que lo anuló.
    revierte_a: int | None
    revertido_por: int | None
    total_debe: Decimal
    total_haber: Decimal
    lineas: list[LineaOut]


class TotalesOut(BaseModel):
    """CUU-004 paso 3 / 3.a: totales del asiento y diferencia entre Debe y Haber."""

    total_debe: Decimal
    total_haber: Decimal
    diferencia: Decimal
    balanceado: bool
