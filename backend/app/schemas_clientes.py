"""Esquemas de la API de clientes (CUU-007)."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from app.models import Cliente, CondicionIva

Texto = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
TextoOpcional = Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
# El formato y el dígito verificador del CUIT se validan en el servicio, con un mensaje claro.
Cuit = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=20)]


class ClienteIn(BaseModel):
    cuit: Cuit
    razon_social: Texto
    condicion_iva: CondicionIva
    domicilio: Texto
    localidad: TextoOpcional = ""
    provincia: TextoOpcional = ""


class ClienteResumen(BaseModel):
    id_cliente: int
    codigo: str
    cuit: str | None
    razon_social: str | None
    activo: bool


class ClienteOut(ClienteResumen):
    condicion_iva: str | None
    domicilio: str | None
    localidad: str | None
    provincia: str | None

    @classmethod
    def de(cls, cliente: Cliente) -> "ClienteOut":
        return cls(
            id_cliente=cliente.id_cliente,
            codigo=cliente.codigo,
            cuit=cliente.cuit,
            razon_social=cliente.razon_social,
            activo=cliente.esta_activo,
            condicion_iva=cliente.condicion_iva,
            domicilio=cliente.domicilio,
            localidad=cliente.localidad,
            provincia=cliente.provincia,
        )


class ClienteDetalleOut(ClienteOut):
    cantidad_comprobantes: int
    comprobantes_pendientes: int


class DatosPadronOut(BaseModel):
    razon_social: str
    condicion_iva: str
    domicilio: str
    localidad: str
    provincia: str


class ConsultaCuitOut(BaseModel):
    """CUU-007 pasos 3-4: datos del padrón de ARCA y, si existe, el cliente ya registrado con ese CUIT."""

    cuit: str
    en_padron: bool
    datos: DatosPadronOut | None
    cliente_existente: ClienteResumen | None


class ComprobanteOut(BaseModel):
    """CUU-007 2.b.2: comprobante asociado al cliente."""

    id_venta: int
    tipo_comprobante: str | None
    numero: str
    fecha_emision: date | None
    moneda: str | None
    importe_total: Decimal | None
    cae: str | None
    asentado: bool
    pendiente: bool


class ValidacionOut(BaseModel):
    valido: bool
    mensaje: str
