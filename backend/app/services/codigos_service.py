"""Códigos de verificación de un solo uso enviados por correo.

CUU-015 pasos 4-6 (segundo factor), 6.a (código inválido o vencido, reenvío) y 1.a.5-1.a.6
(validación de identidad en el recupero de contraseña). También se usa para el cambio de contraseña.

El cliente recibe un "desafío" opaco que identifica el código pendiente; ni el desafío ni el código
se guardan en claro.
"""

import hashlib
import hmac
import math
import secrets
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import auditoria
from app.config import get_settings
from app.correo import EnviadorCorreo
from app.errors import ErrorNegocio
from app.models import CodigoVerificacion, Proposito, Usuario
from app.tiempo import ahora

TABLA = "USUARIO"
CANAL_EMAIL = "EMAIL"

_ACCIONES = {
    Proposito.LOGIN: ("Código de inicio de sesión", "iniciar sesión"),
    Proposito.RECUPERO_PASSWORD: ("Código para restablecer su contraseña", "restablecer su contraseña"),
    Proposito.CAMBIO_PASSWORD: ("Código para cambiar su contraseña", "cambiar su contraseña"),
}


@dataclass
class Desafio:
    desafio: str
    destino: str  # correo enmascarado
    expira_en: int  # segundos
    reenvio_en: int  # segundos hasta poder pedir otro código


def emitir(
    db: Session, usuario: Usuario, proposito: Proposito, enviador: EnviadorCorreo, origen: str | None
) -> Desafio:
    """Genera un código, lo envía al correo del usuario y confirma la transacción.
    Invalida los códigos pendientes del mismo usuario y propósito. Si el envío falla, no se guarda nada."""
    settings = get_settings()
    momento = ahora()
    pendientes = select(CodigoVerificacion).where(
        CodigoVerificacion.id_usuario == usuario.id_usuario,
        CodigoVerificacion.proposito == proposito,
        CodigoVerificacion.usado_en.is_(None),
        CodigoVerificacion.expira > momento,
    )
    for previo in db.scalars(pendientes):
        previo.expira = momento

    desafio = secrets.token_urlsafe(32)
    codigo = _generar_codigo()
    db.add(
        CodigoVerificacion(
            id_usuario=usuario.id_usuario,
            proposito=proposito,
            desafio_hash=_hash_desafio(desafio),
            codigo_hash=_hash_codigo(desafio, codigo),
            canal=CANAL_EMAIL,
            destino=usuario.email,
            intentos=0,
            fecha_creacion=momento,
            expira=momento + timedelta(minutes=settings.codigo_vigencia_minutos),
        )
    )
    _enviar(enviador, usuario.email or "", proposito, codigo)
    _auditar(db, "CODIGO_ENVIADO", usuario, proposito, origen)
    db.commit()
    return _desafio(desafio, usuario.email or "")


def reenviar(db: Session, desafio: str, enviador: EnviadorCorreo, origen: str | None) -> Desafio:
    """CUU-015 6.a.2-6.a.3: genera un nuevo código para el mismo desafío."""
    settings = get_settings()
    registro = _buscar(db, desafio)
    if registro is None or registro.usado_en is not None:
        raise ErrorNegocio(400, "La solicitud ya no es válida. Inicie el proceso nuevamente.")
    momento = ahora()
    espera = settings.codigo_reenvio_segundos - (momento - registro.fecha_creacion).total_seconds()
    if espera > 0:
        raise ErrorNegocio(429, f"Espere {math.ceil(espera)} segundo(s) para solicitar un nuevo código.")
    usuario = _usuario_activo(db, registro.id_usuario)

    codigo = _generar_codigo()
    registro.codigo_hash = _hash_codigo(desafio, codigo)
    registro.intentos = 0
    registro.fecha_creacion = momento
    registro.expira = momento + timedelta(minutes=settings.codigo_vigencia_minutos)
    _enviar(enviador, usuario.email or "", Proposito(registro.proposito), codigo)
    _auditar(db, "CODIGO_REENVIADO", usuario, Proposito(registro.proposito), origen)
    db.commit()
    return _desafio(desafio, usuario.email or "")


def validar(
    db: Session,
    desafio: str,
    codigo: str,
    proposito: Proposito,
    origen: str | None,
    usuario_esperado: Usuario | None = None,
) -> Usuario:
    """CUU-015 paso 6 / 6.a.1. Marca el código como usado y devuelve el usuario, sin confirmar la
    transacción (quien llama confirma junto con su propia operación). Un código incorrecto se
    registra y confirma antes de rechazar."""
    settings = get_settings()
    registro = _buscar(db, desafio)
    if (
        registro is None
        or registro.proposito != proposito
        or registro.usado_en is not None
        or (usuario_esperado is not None and registro.id_usuario != usuario_esperado.id_usuario)
    ):
        raise ErrorNegocio(400, "El código no es válido o ya fue utilizado. Solicite uno nuevo.")
    if registro.intentos >= settings.codigo_max_intentos:
        raise ErrorNegocio(400, "Se superó la cantidad de intentos para este código. Solicite uno nuevo.")
    momento = ahora()
    if registro.expira <= momento:
        raise ErrorNegocio(400, "El código venció. Solicite uno nuevo.")

    if not hmac.compare_digest(registro.codigo_hash, _hash_codigo(desafio, codigo.strip())):
        registro.intentos += 1
        usuario = db.get(Usuario, registro.id_usuario)
        if usuario is not None:
            _auditar(db, "CODIGO_INVALIDO", usuario, proposito, origen)
        db.commit()
        restantes = settings.codigo_max_intentos - registro.intentos
        if restantes <= 0:
            raise ErrorNegocio(400, "Código incorrecto. Se superó la cantidad de intentos: solicite un nuevo código.")
        raise ErrorNegocio(400, f"Código incorrecto. Le quedan {restantes} intento(s).")

    registro.usado_en = momento
    return _usuario_activo(db, registro.id_usuario)


def enmascarar(email: str) -> str:
    local, _, dominio = email.partition("@")
    return f"{local[:1]}***@{dominio}" if dominio else "***"


def _buscar(db: Session, desafio: str) -> CodigoVerificacion | None:
    return db.scalar(select(CodigoVerificacion).where(CodigoVerificacion.desafio_hash == _hash_desafio(desafio)))


def _usuario_activo(db: Session, id_usuario: int) -> Usuario:
    usuario = db.get(Usuario, id_usuario)
    if usuario is None or not usuario.esta_activo:
        raise ErrorNegocio(403, "La cuenta está deshabilitada. Contacte al administrador.")
    return usuario


def _desafio(desafio: str, email: str) -> Desafio:
    settings = get_settings()
    return Desafio(
        desafio=desafio,
        destino=enmascarar(email),
        expira_en=settings.codigo_vigencia_minutos * 60,
        reenvio_en=settings.codigo_reenvio_segundos,
    )


def _enviar(enviador: EnviadorCorreo, email: str, proposito: Proposito, codigo: str) -> None:
    asunto, accion = _ACCIONES[proposito]
    minutos = get_settings().codigo_vigencia_minutos
    cuerpo = (
        f"Su código para {accion} en EugenIA es:\n\n"
        f"    {codigo}\n\n"
        f"Vence en {minutos} minutos y puede usarse una sola vez.\n"
        "Si usted no realizó esta solicitud, ignore este mensaje e informe al administrador del sistema."
    )
    enviador.enviar(email, f"EugenIA - {asunto}", cuerpo)


def _auditar(db: Session, accion: str, usuario: Usuario, proposito: Proposito, origen: str | None) -> None:
    auditoria.registrar(
        db,
        accion=accion,
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=usuario.email,
        origen=origen,
        despues={"proposito": str(proposito), "canal": CANAL_EMAIL, "destino": enmascarar(usuario.email or "")},
    )


def _generar_codigo() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _hash_desafio(desafio: str) -> str:
    return hashlib.sha256(desafio.encode()).hexdigest()


def _hash_codigo(desafio: str, codigo: str) -> str:
    clave = get_settings().jwt_secret.encode()
    return hmac.new(clave, f"{desafio}:{codigo}".encode(), hashlib.sha256).hexdigest()
