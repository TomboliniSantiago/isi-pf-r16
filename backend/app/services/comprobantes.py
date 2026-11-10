"""Piezas compartidas por el registro de ventas (CUU-001) y de compras (CUU-002)."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import ErrorNegocio
from app.models import ClavePredeterminada, CuentaPredeterminada, EmpresaEmisora, PlanCuenta

CERO = Decimal("0.00")
MONEDA = "ARS"  # multimoneda fuera del alcance


@dataclass
class LineaPropuesta:
    rol: str
    descripcion: str
    cuenta: PlanCuenta | None
    debe: Decimal
    haber: Decimal


@dataclass
class Propuesta:
    """Asiento que generará el comprobante (pasos 4-6), antes de registrarlo."""

    lineas: list[LineaPropuesta]

    @property
    def total_debe(self) -> Decimal:
        return sum((linea.debe for linea in self.lineas), CERO)

    @property
    def total_haber(self) -> Decimal:
        return sum((linea.haber for linea in self.lineas), CERO)

    @property
    def balanceado(self) -> bool:
        return self.total_debe == self.total_haber and self.total_debe > 0

    @property
    def faltantes(self) -> list[str]:
        return [linea.descripcion for linea in self.lineas if linea.cuenta is None]

    def lineas_out(self) -> list[dict[str, Any]]:
        return [
            {
                "rol": linea.rol,
                "descripcion": linea.descripcion,
                "id_cuenta": linea.cuenta.id_cuenta if linea.cuenta else None,
                "codigo": linea.cuenta.codigo if linea.cuenta else None,
                "nombre": linea.cuenta.nombre if linea.cuenta else None,
                "debe": linea.debe,
                "haber": linea.haber,
            }
            for linea in self.lineas
        ]


class SelectorCuentas:
    """Paso 4: la cuenta que eligió el usuario (4.a) o, si no eligió, la predeterminada para la clave."""

    def __init__(self, db: Session):
        self.db = db
        self.predeterminadas = {p.clave: p.id_cuenta for p in db.scalars(select(CuentaPredeterminada))}

    def cuenta(self, elegida: int | None, clave: ClavePredeterminada) -> PlanCuenta | None:
        id_cuenta = elegida or self.predeterminadas.get(clave)
        if id_cuenta is None:
            return None
        encontrada = self.db.get(PlanCuenta, id_cuenta)
        if encontrada is None:
            raise ErrorNegocio(422, "La cuenta seleccionada no existe.")
        return encontrada


def empresa_emisora(db: Session) -> EmpresaEmisora:
    emisor = db.scalars(select(EmpresaEmisora).order_by(EmpresaEmisora.id_emisor).limit(1)).first()
    if emisor is None:
        raise ErrorNegocio(409, "No hay una empresa emisora configurada.")
    return emisor


def filtro_por_numero(texto: str, columna_punto_venta: Any, columna_numero: Any) -> Any | None:
    """Búsqueda por número de comprobante, con o sin el punto de venta (0001-00000123)."""
    partes = [p for p in texto.replace(" ", "").split("-") if p]
    if len(partes) == 2 and all(p.isdigit() for p in partes):
        return (columna_punto_venta == int(partes[0])) & (columna_numero == int(partes[1]))
    digitos = "".join(c for c in texto if c.isdigit())
    if digitos and len(digitos) <= 8:
        return columna_numero == int(digitos)
    return None


def errores_de_importes(neto: Decimal, fecha_emision: Any, fecha_contable: Any) -> str | None:
    if neto <= 0:
        return "El neto gravado debe ser mayor a cero."
    if fecha_contable and fecha_contable < fecha_emision:
        return "La fecha contable no puede ser anterior a la fecha de emisión."
    return None


def mensaje_faltantes(faltantes: list[str]) -> str:
    return (
        f"No se pudo determinar la cuenta de {', '.join(faltantes)}. "
        "Selecciónela o configúrela como cuenta predeterminada en el Plan de Cuentas."
    )
