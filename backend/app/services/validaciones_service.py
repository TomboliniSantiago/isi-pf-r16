"""CUU-017 Validar comprobante con ARCA, para ventas y compras.

- Pasos 1-2: el comprobante debe estar vigente (no anulado) y tener CAE; se arman los datos fiscales: el emisor
  es la empresa en una venta y el proveedor en una compra.
- Pasos 3-4: la consulta va al adaptador de ARCA (app.arca.comprobantes), desacoplado de esta lógica. Antes de
  enviarla, el comprobante queda EN_VALIDACION y el intento se registra en VALIDACION_ARCA (confirmado en la
  base), así el intento queda en el historial aunque ARCA no responda.
- Paso 5: se compara lo que informa ARCA con lo registrado y se verifica la vigencia del CAE.
- Pasos 6-8: se actualiza el estado fiscal y se informa el resultado:
    3.a ARCA no responde o responde con error → ERROR_INTEGRACION (queda pendiente: se puede reintentar).
    4.a el comprobante no existe → INVALIDO.
    6.a los datos difieren → PENDIENTE_AUDITORIA, con las diferencias.
    5.a el CAE vencía antes de la fecha de emisión → OBSERVADO.
    Si no, VALIDO.
- El estado fiscal no condiciona la contabilización (decisión del 20/11/2026): solo se informa.
- Reintento controlado: no se valida un comprobante que ya tiene una consulta en curso. Si quedó EN_VALIDACION
  sin respuesta (por ejemplo, se cortó el proceso), pasado el tiempo configurado se da por interrumpida.
"""

import json
import logging
from datetime import timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import auditoria
from app.arca.comprobantes import (
    CODIGO_TIPO,
    ArcaNoDisponible,
    DatosComprobante,
    ErrorArca,
    RespuestaArca,
    ServicioComprobantes,
)
from app.config import get_settings
from app.errors import ErrorNegocio
from app.models import (
    Cliente,
    Compra,
    EstadoCompra,
    EstadoFiscal,
    EstadoVenta,
    Proveedor,
    Usuario,
    ValidacionArca,
    Venta,
)
from app.services.comprobantes import empresa_emisora
from app.tiempo import ahora

log = logging.getLogger(__name__)

VENTA = "VENTA"
COMPRA = "COMPRA"

# Campos que se comparan con lo que informa ARCA (paso 5 / 6.a).
CAMPOS_COMPARADOS = {
    "cuit_emisor": "CUIT del emisor",
    "tipo_comprobante": "Tipo de comprobante",
    "punto_venta": "Punto de venta",
    "numero": "Número",
    "fecha_emision": "Fecha de emisión",
    "importe_total": "Importe total",
    "cae": "CAE",
}

Comprobante = Venta | Compra


def obtener_comprobante(db: Session, tabla: str, id_comprobante: int) -> Comprobante:
    modelo = Venta if tabla == VENTA else Compra
    comprobante = db.get(modelo, id_comprobante)
    if comprobante is None:
        raise ErrorNegocio(404, f"La {tabla.lower()} no existe.")
    return comprobante


def historial(db: Session, tabla: str, id_comprobante: int) -> list[ValidacionArca]:
    """Intentos de validación del comprobante, del más reciente al más antiguo (base de CUU-022)."""
    obtener_comprobante(db, tabla, id_comprobante)
    consulta = (
        select(ValidacionArca)
        .where(ValidacionArca.tabla_comprobante == tabla, ValidacionArca.id_comprobante == id_comprobante)
        .order_by(ValidacionArca.id_validacion.desc())
    )
    return list(db.scalars(consulta))


def validar(
    db: Session,
    tabla: str,
    id_comprobante: int,
    servicio: ServicioComprobantes,
    actor: Usuario,
    origen: str | None,
) -> ValidacionArca:
    comprobante = obtener_comprobante(db, tabla, id_comprobante)
    consulta = _consulta(db, tabla, comprobante)  # pasos 1-2
    _rechazar_consulta_en_curso(db, tabla, comprobante)
    estado_anterior = comprobante.estado_fiscal or EstadoFiscal.PENDIENTE

    validacion = ValidacionArca(
        tabla_comprobante=tabla,
        id_comprobante=id_comprobante,
        id_usuario=actor.id_usuario,
        fecha_inicio=ahora(),
        estado=EstadoFiscal.EN_VALIDACION,
        consulta=_json(_enviado(consulta)),
    )
    db.add(validacion)
    comprobante.estado_fiscal = EstadoFiscal.EN_VALIDACION
    db.commit()

    respuesta: RespuestaArca | None = None
    diferencias: list[dict[str, Any]] = []
    try:
        respuesta = servicio.consultar(consulta)  # pasos 3-4
        estado, mensaje, diferencias = _evaluar(comprobante, consulta, respuesta)  # paso 5
    except ArcaNoDisponible:
        estado = EstadoFiscal.ERROR_INTEGRACION
        mensaje = "No fue posible establecer conexión con ARCA: el comprobante queda pendiente de validación."
    except ErrorArca as exc:
        estado = EstadoFiscal.ERROR_INTEGRACION
        mensaje = f"ARCA respondió con un error ({exc}): el comprobante queda pendiente de validación."
    except Exception:  # cualquier falla del adaptador se registra como error de integración
        log.exception("Error inesperado al consultar ARCA (%s %s)", tabla, id_comprobante)
        estado = EstadoFiscal.ERROR_INTEGRACION
        mensaje = "Error inesperado al consultar ARCA: el comprobante queda pendiente de validación."

    validacion.estado = estado
    validacion.mensaje = mensaje[:500]
    validacion.fecha_respuesta = ahora()
    validacion.respuesta = _json(_recibido(respuesta)) if respuesta else None
    validacion.diferencias = _json(diferencias) if diferencias else None
    comprobante.estado_fiscal = estado
    # El vencimiento del CAE se completa con el que informa ARCA si el comprobante no lo tenía.
    autorizado = respuesta.comprobante if respuesta else None
    if autorizado and autorizado.cae_vencimiento and comprobante.cae_vencimiento is None and not diferencias:
        comprobante.cae_vencimiento = autorizado.cae_vencimiento
    auditoria.registrar(
        db,
        accion="VALIDACION_ARCA",
        tabla=tabla,
        id_registro=id_comprobante,
        actor=actor.email,
        origen=origen,
        antes={"estado_fiscal": estado_anterior},
        despues={
            "estado_fiscal": estado,
            "id_validacion": validacion.id_validacion,
            "mensaje": validacion.mensaje,
            "diferencias": diferencias or None,
        },
    )
    db.commit()
    return validacion


# ---------- Auxiliares ----------


def _consulta(db: Session, tabla: str, comprobante: Comprobante) -> DatosComprobante:
    nombre = "la venta" if tabla == VENTA else "la compra"
    if comprobante.estado in (EstadoVenta.ANULADA, EstadoCompra.ANULADA):
        raise ErrorNegocio(409, f"No se valida {nombre}: está anulada.")
    if not comprobante.cae:
        raise ErrorNegocio(422, f"Para validar {nombre} con ARCA, cargue primero su CAE.")
    empresa = empresa_emisora(db)
    if isinstance(comprobante, Venta):
        cliente = db.get(Cliente, comprobante.id_cliente)
        emisor, receptor = empresa.cuit, cliente.cuit if cliente else None
        falta_emisor = "La empresa no tiene CUIT configurado."
    else:
        proveedor = db.get(Proveedor, comprobante.id_proveedor)
        emisor, receptor = (proveedor.cuit if proveedor else None), empresa.cuit
        falta_emisor = "El proveedor no tiene CUIT: complételo en Proveedores."
    if not emisor:
        raise ErrorNegocio(422, falta_emisor)
    if comprobante.tipo_comprobante not in CODIGO_TIPO:
        raise ErrorNegocio(422, f"ARCA no valida comprobantes de tipo {comprobante.tipo_comprobante}.")
    obligatorios = (comprobante.punto_venta, comprobante.numero_comprobante, comprobante.fecha_emision)
    if any(v is None for v in obligatorios) or comprobante.importe_total is None:
        raise ErrorNegocio(422, f"Los datos de {nombre} están incompletos: modifíquela antes de validarla.")
    return DatosComprobante(
        cuit_emisor=emisor,
        tipo_comprobante=comprobante.tipo_comprobante,
        punto_venta=comprobante.punto_venta,
        numero=comprobante.numero_comprobante,
        fecha_emision=comprobante.fecha_emision,
        importe_total=comprobante.importe_total,
        cae=comprobante.cae,
        cuit_receptor=receptor,
    )


def _rechazar_consulta_en_curso(db: Session, tabla: str, comprobante: Comprobante) -> None:
    if comprobante.estado_fiscal != EstadoFiscal.EN_VALIDACION:
        return
    id_comprobante = comprobante.id_venta if isinstance(comprobante, Venta) else comprobante.id_compra
    en_curso = db.scalars(
        select(ValidacionArca).where(
            ValidacionArca.tabla_comprobante == tabla,
            ValidacionArca.id_comprobante == id_comprobante,
            ValidacionArca.estado == EstadoFiscal.EN_VALIDACION,
        )
    ).all()
    limite = ahora() - timedelta(seconds=get_settings().arca_validacion_vencida_segundos)
    if any(v.fecha_inicio > limite for v in en_curso):
        raise ErrorNegocio(409, "El comprobante ya se está validando con ARCA: espere el resultado.")
    for v in en_curso:  # quedaron sin respuesta: se dan por interrumpidas
        v.estado = EstadoFiscal.ERROR_INTEGRACION
        v.mensaje = "La consulta a ARCA se interrumpió sin respuesta."
        v.fecha_respuesta = ahora()


def _evaluar(
    comprobante: Comprobante, consulta: DatosComprobante, respuesta: RespuestaArca
) -> tuple[EstadoFiscal, str, list[dict[str, Any]]]:
    if not respuesta.existe or respuesta.comprobante is None:  # 4.a
        detalle = " ".join(respuesta.observaciones)
        return EstadoFiscal.INVALIDO, f"ARCA informa que el comprobante no existe. {detalle}".strip(), []
    autorizado = respuesta.comprobante
    diferencias = [
        {"campo": campo, "etiqueta": etiqueta, "registrado": _texto(registrado), "arca": _texto(informado)}
        for campo, etiqueta in CAMPOS_COMPARADOS.items()
        if (registrado := getattr(consulta, campo)) != (informado := getattr(autorizado, campo))
    ]
    vencimiento = autorizado.cae_vencimiento
    if comprobante.cae_vencimiento and vencimiento and comprobante.cae_vencimiento != vencimiento:
        diferencias.append(
            {
                "campo": "cae_vencimiento",
                "etiqueta": "Vencimiento del CAE",
                "registrado": _texto(comprobante.cae_vencimiento),
                "arca": _texto(vencimiento),
            }
        )
    if diferencias:  # 6.a
        return (
            EstadoFiscal.PENDIENTE_AUDITORIA,
            "Los datos informados por ARCA difieren de los registrados: el comprobante queda pendiente de auditoría.",
            diferencias,
        )
    if vencimiento and vencimiento < consulta.fecha_emision:  # 5.a
        return (
            EstadoFiscal.OBSERVADO,
            f"El CAE venció el {vencimiento:%d/%m/%Y}, antes de la fecha de emisión del comprobante "
            f"({consulta.fecha_emision:%d/%m/%Y}): el comprobante queda observado.",
            [],
        )
    return EstadoFiscal.VALIDO, "ARCA confirma el comprobante: los datos coinciden y el CAE está vigente.", []


def _enviado(consulta: DatosComprobante) -> dict[str, Any]:
    return {
        "CuitEmisor": consulta.cuit_emisor,
        "CbteTipo": CODIGO_TIPO.get(consulta.tipo_comprobante),
        "PtoVta": consulta.punto_venta,
        "CbteNro": consulta.numero,
        "CbteFch": consulta.fecha_emision,
        "ImpTotal": consulta.importe_total,
        "CodAutorizacion": consulta.cae,
        "DocNroReceptor": consulta.cuit_receptor,
    }


def _recibido(respuesta: RespuestaArca) -> dict[str, Any]:
    c = respuesta.comprobante
    return {
        "existe": respuesta.existe,
        "observaciones": list(respuesta.observaciones),
        "comprobante": None
        if c is None
        else {
            "cuit_emisor": c.cuit_emisor,
            "tipo_comprobante": c.tipo_comprobante,
            "punto_venta": c.punto_venta,
            "numero": c.numero,
            "fecha_emision": c.fecha_emision,
            "importe_total": c.importe_total,
            "cae": c.cae,
            "cae_vencimiento": c.cae_vencimiento,
        },
    }


def _texto(valor: Any) -> str | None:
    if valor is None:
        return None
    return f"{valor:%d/%m/%Y}" if hasattr(valor, "strftime") else str(valor)


def _json(valor: Any) -> str:
    return json.dumps(valor, ensure_ascii=False, default=str)
