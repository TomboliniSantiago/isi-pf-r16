"""Esquemas de la API del Plan de Cuentas (CUU-005)."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from app.models import ClavePredeterminada, Naturaleza, PlanCuenta, TipoCuenta

# El formato del código (segmentos numéricos separados por punto) se valida en el servicio,
# para informarlo con un mensaje claro (CUU-005 4.b).
Codigo = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
Nombre = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]


class CuentaIn(BaseModel):
    codigo: Codigo
    nombre: Nombre
    tipo_cuenta: TipoCuenta
    naturaleza: Naturaleza | None = None
    imputable: bool
    id_cuenta_padre: int | None = None


class CuentaResumen(BaseModel):
    id_cuenta: int
    codigo: str | None
    nombre: str | None


class CuentaOut(BaseModel):
    id_cuenta: int
    codigo: str | None
    nombre: str | None
    tipo_cuenta: str | None
    naturaleza: str | None
    imputable: bool
    activa: bool
    id_cuenta_padre: int | None
    codigo_padre: str | None
    nivel: int

    @classmethod
    def de(cls, cuenta: PlanCuenta, codigo_padre: str | None) -> "CuentaOut":
        return cls(
            id_cuenta=cuenta.id_cuenta,
            codigo=cuenta.codigo,
            nombre=cuenta.nombre,
            tipo_cuenta=cuenta.tipo_cuenta,
            naturaleza=cuenta.naturaleza,
            imputable=cuenta.es_imputable,
            activa=cuenta.esta_activa,
            id_cuenta_padre=cuenta.id_cuenta_padre,
            codigo_padre=codigo_padre,
            nivel=len((cuenta.codigo or "").split(".")),
        )


class CuentaDetalleOut(CuentaOut):
    """CUU-005 2.c.1: detalle con la ubicación dentro de la jerarquía."""

    ruta: list[CuentaResumen]
    cantidad_hijas: int
    cantidad_movimientos: int
    predeterminada_para: list[ClavePredeterminada]


class MovimientoOut(BaseModel):
    """CUU-005 2.c.2: movimiento de la cuenta en un asiento."""

    id_asiento: int
    numero_asiento: int | None
    fecha: date | None
    concepto: str | None
    estado: str | None
    debe: Decimal
    haber: Decimal


class ValidacionOut(BaseModel):
    """CUU-005 paso 5 / 2.a.4: resultado de las validaciones antes de confirmar."""

    valido: bool
    mensaje: str


class PredeterminadaOut(BaseModel):
    clave: ClavePredeterminada
    descripcion: str
    cuenta: CuentaResumen | None
    # Regla de coherencia: la cuenta asignada debe ser de uno de estos tipos y, si se indica, de esta naturaleza.
    tipos_admitidos: list[TipoCuenta]
    naturaleza: Naturaleza | None
    requisito: str


class PredeterminadaIn(BaseModel):
    id_cuenta: int | None
