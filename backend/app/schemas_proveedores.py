"""Esquemas de la API de proveedores (CUU-008)."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models import CondicionIva, Proveedor
from app.schemas_clientes import Cuit, DatosPadronOut, Texto, TextoOpcional, ValidacionOut

__all__ = ["DatosPadronOut", "ValidacionOut"]


class ProveedorIn(BaseModel):
    cuit: Cuit
    razon_social: Texto
    condicion_iva: CondicionIva
    domicilio: Texto
    localidad: TextoOpcional = ""
    provincia: TextoOpcional = ""


class ProveedorResumen(BaseModel):
    id_proveedor: int
    codigo: str
    cuit: str | None
    razon_social: str | None
    activo: bool


class ProveedorOut(ProveedorResumen):
    condicion_iva: str | None
    domicilio: str | None
    localidad: str | None
    provincia: str | None

    @classmethod
    def de(cls, proveedor: Proveedor) -> "ProveedorOut":
        return cls(
            id_proveedor=proveedor.id_proveedor,
            codigo=proveedor.codigo,
            cuit=proveedor.cuit,
            razon_social=proveedor.razon_social,
            activo=proveedor.esta_activo,
            condicion_iva=proveedor.condicion_iva,
            domicilio=proveedor.domicilio,
            localidad=proveedor.localidad,
            provincia=proveedor.provincia,
        )


class ProveedorDetalleOut(ProveedorOut):
    cantidad_comprobantes: int
    comprobantes_pendientes: int


class ConsultaCuitOut(BaseModel):
    """CUU-008 pasos 3-4: datos del padrón de ARCA y, si existe, el proveedor ya registrado con ese CUIT."""

    cuit: str
    en_padron: bool
    datos: DatosPadronOut | None
    proveedor_existente: ProveedorResumen | None


class ComprobanteOut(BaseModel):
    """CUU-008 2.c.2: comprobante de compra asociado al proveedor."""

    id_compra: int
    tipo_comprobante: str | None
    numero: str
    fecha_emision: date | None
    moneda: str | None
    importe_total: Decimal | None
    asentado: bool
    pendiente: bool
