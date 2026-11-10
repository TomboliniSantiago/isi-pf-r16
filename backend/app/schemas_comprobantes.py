"""Esquemas compartidos por los comprobantes de venta (CUU-001) y de compra (CUU-002)."""

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class TipoComprobante(StrEnum):
    FACTURA_A = "Factura A"
    FACTURA_B = "Factura B"
    FACTURA_C = "Factura C"


class CondicionPago(StrEnum):
    """Condición de cobro (ventas) o de pago (compras). Define la cuenta de contrapartida del asiento."""

    CONTADO = "Contado"  # Caja
    CUENTA_CORRIENTE = "Cuenta Corriente"  # Deudores por ventas / Proveedores
    TRANSFERENCIA = "Transferencia"  # Banco


class AsientoComprobanteOut(BaseModel):
    id_asiento: int
    numero_asiento: int | None
    estado: str | None
    # Si el comprobante se anuló: número del contra-asiento que revirtió al asiento.
    revertido_por: int | None


class LineaPropuestaOut(BaseModel):
    """Línea del asiento que generará el comprobante. Sin cuenta: el sistema no pudo determinarla (4.a / 4.b)."""

    rol: str
    descripcion: str
    id_cuenta: int | None
    codigo: str | None
    nombre: str | None
    debe: Decimal
    haber: Decimal
