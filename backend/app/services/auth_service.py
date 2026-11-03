"""CUU-015 Iniciar sesión, con segundo factor por correo y recupero de contraseña (1.a)."""

import math
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import auditoria
from app.config import get_settings
from app.correo import EnviadorCorreo
from app.errors import ErrorNegocio
from app.models import Proposito, Usuario
from app.security import hash_password, validar_politica, verificar_password
from app.services import codigos_service
from app.services.codigos_service import Desafio
from app.tiempo import ahora

TABLA = "USUARIO"
MENSAJE_SIN_CUENTA = "El correo ingresado no tiene una cuenta asignada. Contacte al administrador."


def iniciar_login(db: Session, email: str, password: str, enviador: EnviadorCorreo, origen: str | None) -> Desafio:
    """Pasos 1-4: valida correo y contraseña y envía el código de verificación."""
    usuario = _validar_credenciales(db, email.lower(), password, origen)
    return codigos_service.emitir(db, usuario, Proposito.LOGIN, enviador, origen)


def completar_login(db: Session, desafio: str, codigo: str, origen: str | None) -> Usuario:
    """Pasos 5-7: valida el código y concede el acceso."""
    usuario = codigos_service.validar(db, desafio, codigo, Proposito.LOGIN, origen)
    momento = ahora()
    if usuario.bloqueado_hasta and usuario.bloqueado_hasta > momento:
        raise ErrorNegocio(423, _mensaje_bloqueo(usuario.bloqueado_hasta - momento))
    usuario.ultimo_acceso = momento
    auditoria.registrar(
        db, accion="LOGIN_OK", tabla=TABLA, id_registro=usuario.id_usuario, actor=usuario.email, origen=origen
    )
    db.commit()
    return usuario


def iniciar_recupero(db: Session, email: str, enviador: EnviadorCorreo, origen: str | None) -> Desafio:
    """1.a.1-1.a.5: verifica que el correo exista y envía el código de validación de identidad."""
    usuario = db.scalar(select(Usuario).where(func.lower(Usuario.email) == email.lower()))
    if usuario is None:
        raise ErrorNegocio(404, MENSAJE_SIN_CUENTA)
    if not usuario.esta_activo:
        raise ErrorNegocio(403, "La cuenta está deshabilitada. Contacte al administrador.")
    return codigos_service.emitir(db, usuario, Proposito.RECUPERO_PASSWORD, enviador, origen)


def confirmar_recupero(db: Session, desafio: str, codigo: str, nueva: str, origen: str | None) -> None:
    """1.a.6-1.a.9: valida el código y la nueva contraseña. Desbloquea la cuenta."""
    _verificar_politica(nueva)  # 1.a.9.a: se informa sin consumir el código
    usuario = codigos_service.validar(db, desafio, codigo, Proposito.RECUPERO_PASSWORD, origen)
    usuario.password_hash = hash_password(nueva)
    usuario.debe_cambiar_password = False
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    auditoria.registrar(
        db, accion="RECUPERO_PASSWORD", tabla=TABLA, id_registro=usuario.id_usuario, actor=usuario.email, origen=origen
    )
    db.commit()


def solicitar_codigo_cambio(db: Session, usuario: Usuario, enviador: EnviadorCorreo, origen: str | None) -> Desafio:
    return codigos_service.emitir(db, usuario, Proposito.CAMBIO_PASSWORD, enviador, origen)


def cambiar_password(
    db: Session,
    usuario: Usuario,
    actual: str,
    nueva: str,
    desafio: str | None,
    codigo: str | None,
    origen: str | None,
) -> Usuario:
    """El cambio voluntario exige un código enviado por correo. El cambio obligatorio de la
    contraseña temporal no, porque el usuario acaba de validar un código al iniciar sesión."""
    if not verificar_password(actual, usuario.password_hash):
        raise ErrorNegocio(400, "La contraseña actual es incorrecta.")
    _verificar_politica(nueva)
    if verificar_password(nueva, usuario.password_hash):
        raise ErrorNegocio(422, "La nueva contraseña debe ser distinta de la actual.")
    if not usuario.debe_cambiar_password:
        if not desafio or not codigo:
            raise ErrorNegocio(400, "Ingrese el código de verificación enviado a su correo.")
        codigos_service.validar(db, desafio, codigo, Proposito.CAMBIO_PASSWORD, origen, usuario_esperado=usuario)

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


def cerrar_sesion(db: Session, usuario: Usuario, origen: str | None) -> None:
    auditoria.registrar(
        db, accion="LOGOUT", tabla=TABLA, id_registro=usuario.id_usuario, actor=usuario.email, origen=origen
    )
    db.commit()


def _validar_credenciales(db: Session, email: str, password: str, origen: str | None) -> Usuario:
    settings = get_settings()
    usuario = db.scalar(select(Usuario).where(func.lower(Usuario.email) == email))

    if usuario is None:  # 2.a
        _auditar_fallo(db, None, email, origen, "correo no registrado")
        raise ErrorNegocio(401, MENSAJE_SIN_CUENTA)

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
    return usuario


def _verificar_politica(password: str) -> None:
    errores = validar_politica(password)
    if errores:
        raise ErrorNegocio(422, "La contraseña no cumple la política de seguridad: " + " ".join(errores))


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
