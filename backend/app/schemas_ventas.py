"""Esquemas de la API de ventas (CUU-001 Registrar venta)."""

from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas_asientos import Importe


class TipoComprobanteVenta(StrEnum):
    FACTURA_A = "Factura A"
    FACTURA_B = "Factura B"
    FACTURA_C = "Factura C"


class CondicionCobro(StrEnum):
    """Define la cuenta del Debe del asiento (paso 4)."""

    CONTADO = "Contado"  # Caja
    CUENTA_CORRIENTE = "Cuenta Corriente"  # Deudores por ventas
    TRANSFERENCIA = "Transferencia"  # Banco


class CuentasVentaIn(BaseModel):
    """4.a: cuentas que elige el usuario cuando el sistema no puede determinarlas, o para reemplazar
    la cuenta predeterminada. Las que quedan vacías se toman de las cuentas predeterminadas."""

    cobro: int | None = None
    ventas: int | None = None
    iva: int | None = None
    otros_impuestos: int | None = None


class VentaIn(BaseModel):
    """Carga manual del comprobante (camino 1.a). La moneda es siempre pesos (multimoneda fuera de alcance)."""

    id_cliente: int
    tipo_comprobante: TipoComprobanteVenta
    punto_venta: int = Field(ge=1, le=99999)
    numero_comprobante: int = Field(ge=1, le=99999999)
    fecha_emision: date
    # Fecha del asiento; si no se indica, la de emisión.
    fecha_contable: date | None = None
    condicion_venta: CondicionCobro
    importe_neto_gravado: Importe
    importe_iva: Importe = Decimal("0")
    importe_otros_impuestos: Importe = Decimal("0")
    importe_total: Importe
    cuentas: CuentasVentaIn = Field(default_factory=CuentasVentaIn)
    # False: queda pendiente, sin asiento (6.a). True: se contabiliza (pasos 6-7).
    confirmar: bool = False


class ClienteVentaOut(BaseModel):
    id_cliente: int
    codigo: str
    cuit: str | None
    razon_social: str | None


class AsientoVentaOut(BaseModel):
    id_asiento: int
    numero_asiento: int | None
    estado: str | None
    # Si la venta se anuló: número del contra-asiento que revirtió al asiento.
    revertido_por: int | None


class VentaOut(BaseModel):
    id_venta: int
    cliente: ClienteVentaOut | None
    tipo_comprobante: str | None
    punto_venta: int | None
    numero_comprobante: int | None
    numero: str
    fecha_emision: date | None
    fecha_contable: date | None
    condicion_venta: str | None
    moneda: str | None
    importe_neto_gravado: Decimal | None
    importe_iva: Decimal | None
    importe_otros_impuestos: Decimal | None
    importe_total: Decimal | None
    cae: str | None
    estado: str | None
    asiento: AsientoVentaOut | None


class LineaPropuestaOut(BaseModel):
    """Línea del asiento que generará la venta. Sin cuenta: el sistema no pudo determinarla (4.a / 4.b)."""

    rol: str
    descripcion: str
    id_cuenta: int | None
    codigo: str | None
    nombre: str | None
    debe: Decimal
    haber: Decimal


class PropuestaOut(BaseModel):
    """Paso 6: asiento propuesto para revisar antes de confirmar. No guarda nada."""

    lineas: list[LineaPropuestaOut]
    total_debe: Decimal
    total_haber: Decimal
    diferencia: Decimal
    balanceado: bool
    cuentas_faltantes: list[str]
    # 2.a: venta ya registrada con el mismo comprobante.
    duplicado: VentaOut | None
