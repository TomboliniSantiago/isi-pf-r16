import json
from typing import Any

from sqlalchemy.orm import Session

from app.models import AuditoriaLog, Usuario
from app.tiempo import ahora


def instantanea_usuario(usuario: Usuario) -> dict[str, Any]:
    """Valores auditables de un usuario. Nunca incluye el hash de la contraseña."""
    return {
        "nombre_usuario": usuario.nombre_usuario,
        "email": usuario.email,
        "nivel_acceso": usuario.nivel_acceso,
        "activo": usuario.activo,
    }


def registrar(
    db: Session,
    *,
    accion: str,
    tabla: str,
    id_registro: int | None,
    actor: str | None,
    origen: str | None,
    antes: dict[str, Any] | None = None,
    despues: dict[str, Any] | None = None,
) -> None:
    """Agrega un registro de auditoría a la transacción en curso (no hace commit)."""
    db.add(
        AuditoriaLog(
            tabla_afectada=tabla,
            id_registro_afectado=id_registro,
            accion=accion,
            datos_anteriores=_json(antes),
            datos_nuevos=_json(despues),
            fecha_hora=ahora(),
            usuario=actor,
            origen=origen,
        )
    )


def _json(valor: dict[str, Any] | None) -> str | None:
    return None if valor is None else json.dumps(valor, ensure_ascii=False, default=str)
