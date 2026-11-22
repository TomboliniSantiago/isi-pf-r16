"""Esquemas de la validación de comprobantes con ARCA (CUU-017) y su historial (CUU-022)."""

import json
from datetime import date, datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import Usuario, ValidacionArca


class DiferenciaOut(BaseModel):
    """6.a: un dato registrado que no coincide con el que informa ARCA."""

    campo: str
    etiqueta: str
    registrado: str | None
    arca: str | None


class ValidacionArcaOut(BaseModel):
    id_validacion: int
    fecha_inicio: datetime
    fecha_respuesta: datetime | None
    usuario: str | None
    # Estado fiscal resultante (EN_VALIDACION mientras la consulta está en curso).
    estado: str
    mensaje: str | None
    diferencias: list[DiferenciaOut]
    # Vencimiento del CAE según ARCA, si lo informó.
    cae_vencimiento_arca: date | None


def validacion_out(db: Session, validacion: ValidacionArca) -> ValidacionArcaOut:
    usuario = db.get(Usuario, validacion.id_usuario)
    respuesta = json.loads(validacion.respuesta) if validacion.respuesta else {}
    vencimiento = (respuesta.get("comprobante") or {}).get("cae_vencimiento")
    return ValidacionArcaOut(
        id_validacion=validacion.id_validacion,
        fecha_inicio=validacion.fecha_inicio,
        fecha_respuesta=validacion.fecha_respuesta,
        usuario=usuario.email if usuario else None,
        estado=validacion.estado,
        mensaje=validacion.mensaje,
        diferencias=[DiferenciaOut(**d) for d in json.loads(validacion.diferencias or "[]")],
        cae_vencimiento_arca=date.fromisoformat(vencimiento) if vencimiento else None,
    )
