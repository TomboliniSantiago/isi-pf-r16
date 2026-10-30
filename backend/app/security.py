import secrets
import string
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.config import get_settings
from app.errors import ErrorNegocio

PASSWORD_MIN = 8
PASSWORD_MAX_BYTES = 72  # límite de bcrypt


def validar_politica(password: str) -> list[str]:
    """Devuelve las restricciones de la política de contraseñas que no se cumplen."""
    errores = []
    if len(password) < PASSWORD_MIN:
        errores.append(f"Debe tener al menos {PASSWORD_MIN} caracteres.")
    if len(password.encode()) > PASSWORD_MAX_BYTES:
        errores.append(f"No puede superar {PASSWORD_MAX_BYTES} bytes.")
    if not any(c.isupper() for c in password):
        errores.append("Debe incluir al menos una letra mayúscula.")
    if not any(c.islower() for c in password):
        errores.append("Debe incluir al menos una letra minúscula.")
    if not any(c.isdigit() for c in password):
        errores.append("Debe incluir al menos un número.")
    return errores


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=get_settings().bcrypt_rounds)
    return bcrypt.hashpw(password.encode(), salt).decode()


def verificar_password(password: str, password_hash: str | None) -> bool:
    if not password_hash or len(password.encode()) > PASSWORD_MAX_BYTES:
        return False
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:  # hash con formato inválido
        return False


def generar_password_temporal(longitud: int = 12) -> str:
    """Genera una contraseña aleatoria que cumple la política."""
    alfabeto = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alfabeto) for _ in range(longitud))
        if not validar_politica(password):
            return password


def crear_token(id_usuario: int) -> tuple[str, int]:
    """Devuelve el token de acceso y su vigencia en segundos."""
    settings = get_settings()
    emitido = datetime.now(UTC)
    vigencia = timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(id_usuario), "iat": emitido, "exp": emitido + vigencia}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, int(vigencia.total_seconds())


def leer_token(token: str) -> int:
    """Devuelve el id de usuario del token o lanza ErrorNegocio 401."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], options={"require": ["exp", "sub"]}
        )
        return int(payload["sub"])
    except jwt.ExpiredSignatureError as exc:
        raise ErrorNegocio(401, "La sesión expiró. Inicie sesión nuevamente.") from exc
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise ErrorNegocio(401, "Sesión inválida. Inicie sesión nuevamente.") from exc
