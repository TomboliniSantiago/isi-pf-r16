"""Esquemas de la API de comprobantes digitales (CUU-016 Registrar comprobante con OCR/NLP)."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas_asientos import Importe
from app.schemas_comprobantes import CondicionPago, TipoComprobante


class CampoOut(BaseModel):
    campo: str
    etiqueta: str
    valor_extraido: str | None
    # Confianza de la extracción (0 a 1). Por debajo del umbral el campo exige revisión (4.a).
    confianza: Decimal | None
    requiere_revision: bool
    valor_final: str | None
    corregido: bool
    revisado: bool


class ValidacionOut(BaseModel):
    codigo: str
    mensaje: str
    campos: list[str]
    nivel: str


class ContraparteOut(BaseModel):
    """Proveedor (compra) o cliente (venta) identificado por el CUIT extraído."""

    id: int
    codigo: str
    cuit: str | None
    razon_social: str | None
    activo: bool


class ComprobanteAsociadoOut(BaseModel):
    tabla: str
    id: int


class DocumentoOut(BaseModel):
    id_documento: int
    operacion: str | None
    estado: str | None
    nombre_archivo: str | None
    tipo_contenido: str | None
    tamanio_bytes: int | None
    fecha_carga: datetime | None
    fecha_registro: datetime | None
    usuario: str | None
    motor_ocr: str | None
    confianza_ocr: Decimal | None
    aviso_ocr: str | None
    umbral_confianza: float
    campos: list[CampoOut]
    validaciones: list[ValidacionOut]
    contraparte_sugerida: ContraparteOut | None
    comprobante: ComprobanteAsociadoOut | None


class DocumentoResumenOut(BaseModel):
    id_documento: int
    operacion: str | None
    estado: str | None
    nombre_archivo: str | None
    fecha_carga: datetime | None
    usuario: str | None
    comprobante: ComprobanteAsociadoOut | None
    # Resumen de los datos (finales si ya se registró, extraídos si no).
    tipo_comprobante: str | None
    numero: str | None
    razon_social: str | None
    importe_total: str | None


class RegistroDocumentoIn(BaseModel):
    """Pasos 7-8: datos definitivos del comprobante, confirmados o corregidos por el usuario.
    Se registra una compra o venta pendiente (borrador) que luego se revisa y contabiliza (CUU-001/002)."""

    # Proveedor (compra) o cliente (venta): define el CUIT y la razón social definitivos.
    id_contraparte: int
    tipo_comprobante: TipoComprobante
    punto_venta: int = Field(ge=1, le=99999)
    numero_comprobante: int = Field(ge=1, le=99999999)
    fecha_emision: date
    fecha_contable: date | None = None
    condicion: CondicionPago
    importe_neto_gravado: Importe
    importe_iva: Importe = Decimal("0")
    importe_otros_impuestos: Importe = Decimal("0")
    importe_total: Importe
    # 4.a / 6.a: campos marcados para revisión obligatoria que el usuario revisó.
    campos_revisados: list[str] = Field(default_factory=list)
