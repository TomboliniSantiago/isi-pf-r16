"""Envío de correo, desacoplado de la lógica de autenticación.

CORREO_MODO=consola escribe el correo en el log (desarrollo, sin servidor SMTP).
CORREO_MODO=smtp lo envía con smtplib (biblioteca estándar, sin dependencias externas).
Si se pasa `html`, el correo sale multipart: texto plano de respaldo + versión HTML.
"""

import logging
import smtplib
import ssl
from email.message import EmailMessage
from typing import Protocol

from app.config import Settings, get_settings
from app.errors import ErrorNegocio

logger = logging.getLogger("eugenia.correo")


class EnviadorCorreo(Protocol):
    def enviar(self, destinatario: str, asunto: str, cuerpo: str, html: str | None = None) -> None: ...


class CorreoConsola:
    def enviar(self, destinatario: str, asunto: str, cuerpo: str, html: str | None = None) -> None:
        logger.warning("\n[CORREO SIMULADO] Para: %s\nAsunto: %s\n\n%s\n", destinatario, asunto, cuerpo)


class CorreoSmtp:
    def __init__(self, settings: Settings):
        self.s = settings

    def enviar(self, destinatario: str, asunto: str, cuerpo: str, html: str | None = None) -> None:
        mensaje = EmailMessage()
        mensaje["From"] = self.s.smtp_remitente or self.s.smtp_usuario
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(cuerpo)
        if html is not None:
            mensaje.add_alternative(html, subtype="html")
        try:
            if self.s.smtp_seguridad == "ssl":
                servidor: smtplib.SMTP = smtplib.SMTP_SSL(
                    self.s.smtp_host, self.s.smtp_port, timeout=20, context=ssl.create_default_context()
                )
            else:
                servidor = smtplib.SMTP(self.s.smtp_host, self.s.smtp_port, timeout=20)
            with servidor:
                if self.s.smtp_seguridad == "starttls":
                    servidor.starttls(context=ssl.create_default_context())
                if self.s.smtp_usuario:
                    servidor.login(self.s.smtp_usuario, self.s.smtp_password)
                servidor.send_message(mensaje)
        except (smtplib.SMTPException, OSError) as exc:
            logger.error("No se pudo enviar el correo a %s: %s", destinatario, exc)
            raise ErrorNegocio(503, "No fue posible enviar el código por correo. Intente nuevamente.") from exc


def get_enviador() -> EnviadorCorreo:
    settings = get_settings()
    return CorreoSmtp(settings) if settings.correo_modo == "smtp" else CorreoConsola()
