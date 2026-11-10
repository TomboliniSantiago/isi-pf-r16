"""Esquemas de la API de compras (CUU-002 Registrar compra)."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas_asientos import Importe
from app.schemas_comprobantes import AsientoComprobanteOut, CondicionPago, LineaPropuestaOut, TipoComprobante


class CuentasCompraIn(BaseModel):
    """4.a: cuentas que elige el usuario cuando el sistema no puede determinarlas, o para reemplazar
    la cuenta predeterminada. Las que quedan vacías se toman de las cuentas predeterminadas."""

    pago: int | None = None
    compras: int | None = None
    iva: int | None = None
    otros_impuestos: int | None = None


class CompraIn(BaseModel):
    """Carga manual del comprobante del proveedor (camino 1.a). Moneda: pesos (multimoneda fuera de alcance)."""

    id_proveedor: int
    tipo_comprobante: TipoComprobante
    punto_venta: int = Field(ge=1, le=99999)
    numero_comprobante: int = Field(ge=1, le=99999999)
    fecha_emision: date
    # Fecha del asiento; si no se indica, la de emisión.
    fecha_contable: date | None = None
    condicion_compra: CondicionPago
    importe_neto_gravado: Importe
    importe_iva: Importe = Decimal("0")
    importe_otros_impuestos: Importe = Decimal("0")
    importe_total: Importe
    cuentas: CuentasCompraIn = Field(default_factory=CuentasCompraIn)
    # False: queda pendiente, sin asiento (6.a). True: se contabiliza (pasos 6-7).
    confirmar: bool = False


class ProveedorCompraOut(BaseModel):
    id_proveedor: int
    codigo: str
    cuit: str | None
    razon_social: str | None


class CompraOut(BaseModel):
    id_compra: int
    proveedor: ProveedorCompraOut | None
    tipo_comprobante: str | None
    punto_venta: int | None
    numero_comprobante: int | None
    numero: str
    fecha_emision: date | None
    fecha_contable: date | None
    condicion_compra: str | None
    moneda: str | None
    importe_neto_gravado: Decimal | None
    importe_iva: Decimal | None
    importe_otros_impuestos: Decimal | None
    importe_total: Decimal | None
    estado: str | None
    asiento: AsientoComprobanteOut | None


class PropuestaCompraOut(BaseModel):
    """Paso 6: asiento propuesto para revisar antes de confirmar. No guarda nada."""

    lineas: list[LineaPropuestaOut]
    total_debe: Decimal
    total_haber: Decimal
    diferencia: Decimal
    balanceado: bool
    cuentas_faltantes: list[str]
    # 2.a: compra ya registrada con el mismo comprobante del mismo proveedor.
    duplicado: CompraOut | None
