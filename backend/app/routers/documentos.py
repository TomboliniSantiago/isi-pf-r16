from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, Query, Request, Response, UploadFile
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import Cliente, Documento, EstadoDocumento, OperacionDocumento, Rol, Usuario
from app.ocr import interprete
from app.ocr.motor import MotorOcr, get_motor
from app.schemas_documentos import (
    CampoOut,
    ComprobanteAsociadoOut,
    ContraparteOut,
    DocumentoOut,
    DocumentoResumenOut,
    RegistroDocumentoIn,
    ValidacionOut,
)
from app.services import documentos_service as servicio

router = APIRouter(prefix="/api/documentos", tags=["Comprobantes digitales"])
# Consulta: cualquier usuario con sesión. Carga, registro y descarte: actores de CUU-016.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


def _comprobante(documento: Documento) -> ComprobanteAsociadoOut | None:
    if documento.tabla_asociada and documento.id_registro_asociado:
        return ComprobanteAsociadoOut(tabla=documento.tabla_asociada, id=documento.id_registro_asociado)
    return None


def _nombre_usuario(db: Session, id_usuario: int) -> str | None:
    usuario = db.get(Usuario, id_usuario)
    return usuario.nombre_usuario if usuario else None


def _salida(db: Session, documento: Documento) -> DocumentoOut:
    campos = servicio.campos_de(db, [documento.id_documento])[documento.id_documento]
    revisar = servicio.requieren_revision(campos)
    sugerida = (
        servicio.contraparte_sugerida(db, documento, campos)
        if documento.estado == EstadoDocumento.PENDIENTE_REVISION
        else None
    )
    return DocumentoOut(
        id_documento=documento.id_documento,
        operacion=documento.operacion,
        estado=documento.estado,
        nombre_archivo=documento.nombre_archivo,
        tipo_contenido=documento.tipo_contenido,
        tamanio_bytes=documento.tamanio_bytes,
        fecha_carga=documento.fecha_carga,
        fecha_registro=documento.fecha_registro,
        usuario=_nombre_usuario(db, documento.id_usuario),
        motor_ocr=documento.motor_ocr,
        confianza_ocr=documento.confianza_ocr,
        aviso_ocr=documento.aviso_ocr,
        umbral_confianza=get_settings().ocr_umbral_confianza,
        campos=[
            CampoOut(
                campo=c.campo,
                etiqueta=interprete.ETIQUETAS.get(c.campo, c.campo),
                valor_extraido=c.valor_extraido,
                confianza=c.confianza,
                requiere_revision=c.campo in revisar,
                valor_final=c.valor_final,
                corregido=bool(c.corregido),
                revisado=bool(c.revisado),
            )
            for c in campos
        ],
        validaciones=[
            ValidacionOut(codigo=v.codigo, mensaje=v.mensaje, campos=v.campos, nivel=v.nivel)
            for v in servicio.validaciones_de(campos)
        ],
        contraparte_sugerida=ContraparteOut(
            id=sugerida.id_cliente if isinstance(sugerida, Cliente) else sugerida.id_proveedor,
            codigo=sugerida.codigo,
            cuit=sugerida.cuit,
            razon_social=sugerida.razon_social,
            activo=sugerida.esta_activo,
        )
        if sugerida
        else None,
        comprobante=_comprobante(documento),
    )


@router.post("", response_model=DocumentoOut, status_code=201)
async def cargar(
    request: Request,
    archivo: UploadFile = File(...),
    operacion: OperacionDocumento = Form(...),
    actor: Usuario = Depends(puede_editar),
    motor: MotorOcr = Depends(get_motor),
    db: Session = Depends(get_db),
) -> DocumentoOut:
    """CUU-016 pasos 1-5: guarda el archivo original, extrae los datos y los devuelve para revisión."""
    maximo = get_settings().comprobante_max_mb * 1024 * 1024
    contenido = await archivo.read(maximo + 1)
    documento = servicio.cargar(db, contenido, archivo.filename, operacion, motor, actor, origen_de(request))
    return _salida(db, documento)


@router.get("", response_model=list[DocumentoResumenOut])
def listar(
    estado: EstadoDocumento | None = None,
    operacion: OperacionDocumento | None = None,
    tabla_asociada: str | None = None,
    id_registro: int | None = None,
    limite: int = Query(500, ge=1, le=2000),
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[DocumentoResumenOut]:
    documentos = servicio.listar(db, estado, operacion, tabla_asociada, id_registro, limite)
    campos = servicio.campos_de(db, [d.id_documento for d in documentos])
    return [
        DocumentoResumenOut(
            id_documento=d.id_documento,
            operacion=d.operacion,
            estado=d.estado,
            nombre_archivo=d.nombre_archivo,
            fecha_carga=d.fecha_carga,
            usuario=_nombre_usuario(db, d.id_usuario),
            comprobante=_comprobante(d),
            **servicio.resumen(campos[d.id_documento]),
        )
        for d in documentos
    ]


@router.get("/{id_documento}", response_model=DocumentoOut)
def obtener(id_documento: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)) -> DocumentoOut:
    return _salida(db, servicio.obtener(db, id_documento))


@router.get("/{id_documento}/archivo")
def archivo(id_documento: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)) -> Response:
    """Archivo original del comprobante, para verlo junto a los datos extraídos."""
    documento = servicio.obtener(db, id_documento)
    nombre = quote(documento.nombre_archivo or f"comprobante-{id_documento}")
    return Response(
        content=servicio.leer_archivo(documento),
        media_type=documento.tipo_contenido or "application/octet-stream",
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{nombre}", "X-Content-Type-Options": "nosniff"},
    )


@router.post("/{id_documento}/registrar", response_model=DocumentoOut)
def registrar(
    id_documento: int,
    datos: RegistroDocumentoIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> DocumentoOut:
    """CUU-016 pasos 7-11: registra los datos definitivos como compra o venta pendiente (borrador)."""
    return _salida(db, servicio.registrar(db, id_documento, datos, actor, origen_de(request)))


@router.post("/{id_documento}/descartar", response_model=DocumentoOut)
def descartar(
    id_documento: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> DocumentoOut:
    return _salida(db, servicio.descartar(db, id_documento, actor, origen_de(request)))
