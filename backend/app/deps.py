from collections.abc import Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.errors import ErrorNegocio
from app.models import Rol, Usuario
from app.security import leer_token

_bearer = HTTPBearer(auto_error=False)


def origen_de(request: Request) -> str | None:
    return request.client.host if request.client else None


def usuario_autenticado(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    """Usuario del token. Se relee de la base en cada request: una baja o un cambio de rol
    tienen efecto inmediato aunque el token siga vigente."""
    if credenciales is None:
        raise ErrorNegocio(401, "Debe iniciar sesión.")
    usuario = db.get(Usuario, leer_token(credenciales.credentials))
    if usuario is None or not usuario.esta_activo:
        raise ErrorNegocio(401, "Sesión inválida. Inicie sesión nuevamente.")
    return usuario


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
