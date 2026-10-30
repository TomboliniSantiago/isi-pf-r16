"""CUU-015 Iniciar sesión."""

import math
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import auditoria
from app.config import get_settings
from app.errors import ErrorNegocio
from app.models import Usuario
from app.security import hash_password, validar_politica, verificar_password
from app.tiempo import ahora

TABLA = "USUARIO"


def autenticar(db: Session, email: str, password: str, origen: str | None) -> Usuario:
    settings = get_settings()
    email = email.lower()
    usuario = db.scalar(select(Usuario).where(func.lower(Usuario.email) == email))

    if usuario is None:  # 2.a
        _auditar_fallo(db, None, email, origen, "correo no registrado")
        raise ErrorNegocio(401, "El correo ingresado no tiene una cuenta asignada. Contacte al administrador.")

    if not usuario.esta_activo:
        _auditar_fallo(db, usuario.id_usuario, email, origen, "cuenta dada de baja")
        raise ErrorNegocio(403, "La cuenta está deshabilitada. Contacte al administrador.")

    momento = ahora()
    if usuario.bloqueado_hasta and usuario.bloqueado_hasta > momento:  # 3.b.3
        _auditar_fallo(db, usuario.id_usuario, email, origen, "cuenta bloqueada")
        raise ErrorNegocio(423, _mensaje_bloqueo(usuario.bloqueado_hasta - momento))

    if not verificar_password(password, usuario.password_hash):
        usuario.intentos_fallidos = (usuario.intentos_fallidos or 0) + 1
        if usuario.intentos_fallidos >= settings.login_max_intentos:  # 3.b
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = momento + timedelta(minutes=settings.login_bloqueo_minutos)
            auditoria.registrar(
                db,
                accion="BLOQUEO",
                tabla=TABLA,
                id_registro=usuario.id_usuario,
                actor=email,
                origen=origen,
                despues={"bloqueado_hasta": usuario.bloqueado_hasta},
            )
            db.commit()
            raise ErrorNegocio(423, _mensaje_bloqueo(usuario.bloqueado_hasta - momento))
        restantes = settings.login_max_intentos - usuario.intentos_fallidos  # 3.a
        _auditar_fallo(db, usuario.id_usuario, email, origen, "contraseña inválida")
        raise ErrorNegocio(401, f"Contraseña inválida. Le quedan {restantes} intento(s) antes del bloqueo temporal.")

    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    usuario.ultimo_acceso = momento
    auditoria.registrar(db, accion="LOGIN_OK", tabla=TABLA, id_registro=usuario.id_usuario, actor=email, origen=origen)
    db.commit()
    return usuario


def cerrar_sesion(db: Session, usuario: Usuario, origen: str | None) -> None:
    auditoria.registrar(
        db, accion="LOGOUT", tabla=TABLA, id_registro=usuario.id_usuario, actor=usuario.email, origen=origen
    )
    db.commit()


def cambiar_password(db: Session, usuario: Usuario, actual: str, nueva: str, origen: str | None) -> Usuario:
    if not verificar_password(actual, usuario.password_hash):
        raise ErrorNegocio(400, "La contraseña actual es incorrecta.")
    errores = validar_politica(nueva)
    if errores:
        raise ErrorNegocio(422, "La contraseña no cumple la política de seguridad: " + " ".join(errores))
    if verificar_password(nueva, usuario.password_hash):
        raise ErrorNegocio(422, "La nueva contraseña debe ser distinta de la actual.")

    usuario.password_hash = hash_password(nueva)
    usuario.debe_cambiar_password = False
    auditoria.registrar(
        db,
        accion="CAMBIO_PASSWORD",
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=usuario.email,
        origen=origen,
    )
    db.commit()
    return usuario


def _auditar_fallo(db: Session, id_usuario: int | None, email: str, origen: str | None, motivo: str) -> None:
    auditoria.registrar(
        db,
        accion="LOGIN_FALLIDO",
        tabla=TABLA,
        id_registro=id_usuario,
        actor=email,
        origen=origen,
        despues={"motivo": motivo},
    )
    db.commit()


def _mensaje_bloqueo(restante: timedelta) -> str:
    minutos = max(1, math.ceil(restante.total_seconds() / 60))
    return (
        "La cuenta está bloqueada temporalmente por superar los intentos permitidos. "
        f"Podrá volver a intentar en {minutos} minuto(s)."
    )
