"""CUU-016 Registrar comprobante con OCR/NLP.

Flujo: cargar → extraer → revisar → corregir → registrar (borrador de compra o venta) → contabilizar
(desde Compras o Ventas, CUU-001/002). El OCR nunca contabiliza sin confirmación humana.

- Pasos 1-2 / 2.a: se admiten PDF, PNG y JPG (por su contenido) de hasta COMPROBANTE_MAX_MB. El archivo
  original se guarda en el servidor; el mismo archivo no se carga dos veces mientras no esté descartado.
- Pasos 3-5 / 3.a: el adaptador de OCR obtiene el texto y el intérprete extrae los campos con su confianza
  y las validaciones automáticas. Los campos no reconocidos quedan vacíos con confianza nula.
- 4.a / 6.a: los campos con confianza menor al umbral, o involucrados en una validación con error, exigen
  revisión: no se puede registrar el comprobante sin que el usuario los revise.
- Pasos 7-9 / 7.a: al registrar se guardan el valor extraído y el definitivo de cada campo (marcando los
  corregidos), se crea la compra o venta pendiente y se vincula al documento. Todo se audita.
- Descartar es una baja lógica: el documento queda DESCARTADO con su archivo e historial.
"""

from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import almacenamiento, auditoria
from app.config import get_settings
from app.errors import ErrorNegocio
from app.models import (
    Cliente,
    Documento,
    DocumentoCampo,
    EstadoDocumento,
    OperacionDocumento,
    Proveedor,
    TipoDocumento,
    Usuario,
)
from app.ocr import interprete
from app.ocr.motor import TIPO_CONTENIDO, MotorOcr, detectar_formato
from app.schemas_compras import CompraIn
from app.schemas_documentos import RegistroDocumentoIn
from app.schemas_ventas import VentaIn
from app.services import asientos_service, compras_service, ventas_service
from app.services.comprobantes import empresa_emisora
from app.tiempo import ahora

TABLA = "DOCUMENTO"


# ---------- Carga y extracción (pasos 1-5) ----------


def cargar(
    db: Session,
    contenido: bytes,
    nombre_archivo: str | None,
    operacion: OperacionDocumento,
    motor: MotorOcr,
    actor: Usuario,
    origen: str | None,
) -> Documento:
    maximo = get_settings().comprobante_max_mb
    if not contenido:
        raise ErrorNegocio(422, "El archivo está vacío.")
    if len(contenido) > maximo * 1024 * 1024:
        raise ErrorNegocio(422, f"El archivo supera el tamaño máximo de {maximo} MB.")
    formato = detectar_formato(contenido)  # 2.a
    digest = almacenamiento.hash_de(contenido)
    existente = db.scalars(
        select(Documento)
        .where(Documento.hash_sha256 == digest, Documento.estado != EstadoDocumento.DESCARTADO)
        .limit(1)
    ).first()
    if existente:
        raise ErrorNegocio(
            409,
            f"Este archivo ya fue cargado (documento N° {existente.id_documento}, "
            f"{_etiqueta_estado(existente.estado)}).",
        )

    emisor = empresa_emisora(db)
    lectura = motor.leer(contenido, formato)
    resultado = interprete.interpretar(lectura.texto, lectura.confianza, emisor.cuit, emisor.razon_social)

    documento = Documento(
        id_usuario=actor.id_usuario,
        nombre_archivo=(nombre_archivo or f"comprobante.{formato}")[:255],
        ruta_archivo=almacenamiento.guardar(contenido, formato),
        fecha_carga=ahora(),
        operacion=operacion,
        estado=EstadoDocumento.PENDIENTE_REVISION,
        tipo_contenido=TIPO_CONTENIDO[formato],
        tamanio_bytes=len(contenido),
        hash_sha256=digest,
        motor_ocr=lectura.motor,
        confianza_ocr=Decimal(str(round(lectura.confianza, 4))) if lectura.confianza is not None else None,
        aviso_ocr=(lectura.aviso or None) and lectura.aviso[:255],
        texto_extraido=lectura.texto or None,
    )
    db.add(documento)
    db.flush()
    for nombre in interprete.CAMPOS:
        campo = resultado.campos[nombre]
        db.add(
            DocumentoCampo(
                id_documento=documento.id_documento,
                campo=nombre,
                valor_extraido=campo.valor,
                confianza=Decimal(str(campo.confianza)),
                corregido=False,
                revisado=False,
            )
        )
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=documento.id_documento,
        actor=actor.email,
        origen=origen,
        despues={
            "archivo": documento.nombre_archivo,
            "operacion": operacion,
            "motor_ocr": lectura.motor,
            "extraido": {n: resultado.campos[n].valor for n in interprete.CAMPOS},
        },
    )
    db.commit()
    return documento


# ---------- Consulta ----------


def listar(
    db: Session,
    estado: EstadoDocumento | None,
    operacion: OperacionDocumento | None,
    tabla_asociada: str | None,
    id_registro: int | None,
    limite: int = 500,
) -> list[Documento]:
    consulta = select(Documento)
    if estado:
        consulta = consulta.where(Documento.estado == estado)
    if operacion:
        consulta = consulta.where(Documento.operacion == operacion)
    if tabla_asociada:
        consulta = consulta.where(Documento.tabla_asociada == tabla_asociada)
    if id_registro:
        consulta = consulta.where(Documento.id_registro_asociado == id_registro)
    consulta = consulta.order_by(Documento.fecha_carga.desc(), Documento.id_documento.desc()).limit(limite)
    return list(db.scalars(consulta))


def obtener(db: Session, id_documento: int) -> Documento:
    documento = db.get(Documento, id_documento)
    if documento is None:
        raise ErrorNegocio(404, "El documento no existe.")
    return documento


def campos_de(db: Session, ids: list[int]) -> dict[int, list[DocumentoCampo]]:
    resultado: dict[int, list[DocumentoCampo]] = {i: [] for i in ids}
    if ids:
        for campo in db.scalars(select(DocumentoCampo).where(DocumentoCampo.id_documento.in_(ids))):
            resultado[campo.id_documento].append(campo)
    orden = {nombre: i for i, nombre in enumerate(interprete.CAMPOS)}
    for lista in resultado.values():
        lista.sort(key=lambda c: orden.get(c.campo, len(orden)))
    return resultado


def validaciones_de(campos: list[DocumentoCampo]) -> list[interprete.Validacion]:
    """Validaciones automáticas sobre los valores extraídos (paso 4)."""
    return interprete.validar({c.campo: c.valor_extraido for c in campos})


def requieren_revision(campos: list[DocumentoCampo]) -> set[str]:
    """4.a / 6.a: confianza menor al umbral o campo involucrado en una validación con error."""
    umbral = Decimal(str(get_settings().ocr_umbral_confianza))
    bajos = {c.campo for c in campos if c.confianza is None or c.confianza < umbral}
    con_error = {n for v in validaciones_de(campos) if v.nivel == "error" for n in v.campos}
    return bajos | con_error


def contraparte_sugerida(db: Session, documento: Documento, campos: list[DocumentoCampo]) -> Proveedor | Cliente | None:
    """Paso 3 de CUU-001/002: identifica al proveedor o cliente por el CUIT extraído."""
    cuit = next((c.valor_extraido for c in campos if c.campo == "cuit"), None)
    if not cuit:
        return None
    digitos = "".join(ch for ch in cuit if ch.isdigit())
    modelo = Proveedor if documento.operacion == OperacionDocumento.COMPRA else Cliente
    return db.scalars(select(modelo).where(func.replace(modelo.cuit, "-", "") == digitos).limit(1)).first()


def leer_archivo(documento: Documento) -> bytes:
    if not documento.ruta_archivo:
        raise ErrorNegocio(404, "El documento no tiene archivo asociado.")
    return almacenamiento.leer(documento.ruta_archivo)


# ---------- Registro (pasos 7-11) ----------


def registrar(
    db: Session, id_documento: int, datos: RegistroDocumentoIn, actor: Usuario, origen: str | None
) -> Documento:
    documento = obtener(db, id_documento)
    if documento.estado != EstadoDocumento.PENDIENTE_REVISION:
        raise ErrorNegocio(409, f"El documento ya está {_etiqueta_estado(documento.estado)}.")
    campos = campos_de(db, [documento.id_documento])[documento.id_documento]
    faltan = [c for c in interprete.CAMPOS if c in requieren_revision(campos) and c not in datos.campos_revisados]
    if faltan:
        raise ErrorNegocio(
            422,
            "Revise los campos marcados antes de registrar: "
            + ", ".join(interprete.ETIQUETAS[c] for c in faltan)
            + ".",
        )

    if documento.operacion == OperacionDocumento.COMPRA:
        contraparte: Proveedor | Cliente | None = db.get(Proveedor, datos.id_contraparte)
        comprobante = compras_service.crear(
            db,
            CompraIn(id_proveedor=datos.id_contraparte, condicion_compra=datos.condicion, **_importes(datos)),
            actor,
            origen,
            confirmar_transaccion=False,
        )
        tabla, id_registro = "COMPRA", comprobante.id_compra
    else:
        contraparte = db.get(Cliente, datos.id_contraparte)
        comprobante = ventas_service.crear(
            db,
            VentaIn(id_cliente=datos.id_contraparte, condicion_venta=datos.condicion, **_importes(datos)),
            actor,
            origen,
            confirmar_transaccion=False,
        )
        tabla, id_registro = "VENTA", comprobante.id_venta

    finales = _valores_finales(datos, contraparte)
    corregidos: dict[str, tuple[str | None, str | None]] = {}
    for campo in campos:
        final = finales.get(campo.campo)
        campo.valor_final = final
        campo.corregido = not _iguales(campo.campo, campo.valor_extraido, final)
        campo.revisado = campo.campo in datos.campos_revisados
        if campo.corregido:
            corregidos[campo.campo] = (campo.valor_extraido, final)

    documento.estado = EstadoDocumento.REGISTRADO
    documento.tabla_asociada = tabla
    documento.id_registro_asociado = id_registro
    documento.fecha_registro = ahora()
    tipo = db.scalars(select(TipoDocumento).where(TipoDocumento.nombre == datos.tipo_comprobante).limit(1)).first()
    documento.id_tipo_documento = tipo.id_tipo_documento if tipo else None

    if corregidos:  # 7.a.3: correcciones auditadas con el valor extraído y el corregido
        auditoria.registrar(
            db,
            accion="CORRECCION",
            tabla=TABLA,
            id_registro=documento.id_documento,
            actor=actor.email,
            origen=origen,
            antes={c: extraido for c, (extraido, _) in corregidos.items()},
            despues={c: final for c, (_, final) in corregidos.items()},
        )
    auditoria.registrar(
        db,
        accion="REGISTRO",
        tabla=TABLA,
        id_registro=documento.id_documento,
        actor=actor.email,
        origen=origen,
        despues={
            "comprobante": f"{tabla} {id_registro}",
            "campos_corregidos": sorted(corregidos),
            "campos_revisados": sorted(datos.campos_revisados),
        },
    )
    asientos_service.confirmar_transaccion(db)
    return documento


def descartar(db: Session, id_documento: int, actor: Usuario, origen: str | None) -> Documento:
    documento = obtener(db, id_documento)
    if documento.estado != EstadoDocumento.PENDIENTE_REVISION:
        raise ErrorNegocio(
            409, f"Solo se descartan documentos pendientes de revisión; este está {_etiqueta_estado(documento.estado)}."
        )
    documento.estado = EstadoDocumento.DESCARTADO
    auditoria.registrar(
        db,
        accion="DESCARTE",
        tabla=TABLA,
        id_registro=documento.id_documento,
        actor=actor.email,
        origen=origen,
        antes={"estado": EstadoDocumento.PENDIENTE_REVISION},
        despues={"estado": EstadoDocumento.DESCARTADO},
    )
    db.commit()
    return documento


# ---------- Auxiliares ----------


def _importes(datos: RegistroDocumentoIn) -> dict[str, Any]:
    return {
        "tipo_comprobante": datos.tipo_comprobante,
        "punto_venta": datos.punto_venta,
        "numero_comprobante": datos.numero_comprobante,
        "fecha_emision": datos.fecha_emision,
        "fecha_contable": datos.fecha_contable,
        "importe_neto_gravado": datos.importe_neto_gravado,
        "importe_iva": datos.importe_iva,
        "importe_otros_impuestos": datos.importe_otros_impuestos,
        "importe_total": datos.importe_total,
        "confirmar": False,  # borrador: se contabiliza después de revisar el asiento (CUU-001/002)
    }


def _valores_finales(datos: RegistroDocumentoIn, contraparte: Proveedor | Cliente | None) -> dict[str, str | None]:
    return {
        "cuit": contraparte.cuit if contraparte else None,
        "razon_social": contraparte.razon_social if contraparte else None,
        "tipo_comprobante": str(datos.tipo_comprobante),
        "punto_venta": str(datos.punto_venta),
        "numero_comprobante": str(datos.numero_comprobante),
        "fecha_emision": datos.fecha_emision.isoformat(),
        "importe_neto_gravado": f"{datos.importe_neto_gravado:.2f}",
        "importe_iva": f"{datos.importe_iva:.2f}",
        "importe_otros_impuestos": f"{datos.importe_otros_impuestos:.2f}",
        "importe_total": f"{datos.importe_total:.2f}",
    }


def _iguales(campo: str, extraido: str | None, final: str | None) -> bool:
    if campo in interprete.IMPORTES:
        return interprete.a_decimal(extraido) == interprete.a_decimal(final)
    if campo == "cuit":
        return "".join(ch for ch in extraido or "" if ch.isdigit()) == "".join(ch for ch in final or "" if ch.isdigit())
    return (extraido or "").strip().lower() == (final or "").strip().lower()


def _etiqueta_estado(estado: str | None) -> str:
    return {
        EstadoDocumento.PENDIENTE_REVISION: "pendiente de revisión",
        EstadoDocumento.REGISTRADO: "registrado",
        EstadoDocumento.DESCARTADO: "descartado",
    }.get(estado or "", estado or "")


def resumen(campos: list[DocumentoCampo]) -> dict[str, str | None]:
    valores = {c.campo: (c.valor_final if c.valor_final is not None else c.valor_extraido) for c in campos}
    pv, nro = valores.get("punto_venta"), valores.get("numero_comprobante")
    numero = f"{int(pv):04d}-{int(nro):08d}" if pv and nro and pv.isdigit() and nro.isdigit() else None
    return {
        "tipo_comprobante": valores.get("tipo_comprobante"),
        "numero": numero,
        "razon_social": valores.get("razon_social"),
        "importe_total": valores.get("importe_total"),
    }
