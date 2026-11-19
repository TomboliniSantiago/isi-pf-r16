from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ErrorNegocio
from app.models import Rol, SesionRevocada, Usuario
from app.security import DatosToken, leer_token

_bearer = HTTPBearer(auto_error=False)


def origen_de(request: Request) -> str | None:
    return request.client.host if request.client else None


@dataclass(frozen=True)
class Sesion:
    usuario: Usuario
    token: DatosToken


def sesion_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Sesion:
    """Sesión del token. El usuario se relee de la base en cada request: una baja o un cambio de rol
    tienen efecto inmediato aunque el token siga vigente. Un token cerrado con logout se rechaza."""
    if credenciales is None:
        raise ErrorNegocio(401, "Debe iniciar sesión.")
    datos = leer_token(credenciales.credentials)
    revocada = db.scalar(select(SesionRevocada.id_sesion_revocada).where(SesionRevocada.jti == datos.jti))
    if revocada is not None:
        raise ErrorNegocio(401, "La sesión fue cerrada. Inicie sesión nuevamente.")
    usuario = db.get(Usuario, datos.id_usuario)
    if usuario is None or not usuario.esta_activo:
        raise ErrorNegocio(401, "Sesión inválida. Inicie sesión nuevamente.")
    return Sesion(usuario=usuario, token=datos)


def usuario_autenticado(sesion: Sesion = Depends(sesion_actual)) -> Usuario:
    return sesion.usuario


def usuario_habilitado(usuario: Usuario = Depends(usuario_autenticado)) -> Usuario:
    """Como usuario_autenticado, pero exige haber reemplazado la contraseña temporal."""
    if usuario.debe_cambiar_password:
        raise ErrorNegocio(403, "Debe cambiar su contraseña antes de continuar.")
    return usuario


def requiere_roles(*roles: Rol) -> Callable[..., Usuario]:
    def dependencia(usuario: Usuario = Depends(usuario_habilitado)) -> Usuario:
        if usuario.nivel_acceso not in roles:
            raise ErrorNegocio(403, "No tiene permisos para realizar esta operación.")
        return usuario

    return dependencia
