"""Mapeo de las tablas existentes (esquema base + migraciones 001 y 002)."""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

ACTIVO = "S"
INACTIVO = "N"


class Rol(StrEnum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CONTADOR = "CONTADOR"
    ADMINISTRATIVO = "ADMINISTRATIVO"
    CONSULTA = "CONSULTA"


class Usuario(Base):
    __tablename__ = "USUARIO"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_usuario: Mapped[str | None] = mapped_column(Unicode(255))
    password_hash: Mapped[str | None] = mapped_column(Unicode(255))
    email: Mapped[str | None] = mapped_column(Unicode(255))
    nivel_acceso: Mapped[str | None] = mapped_column(Unicode(255))
    activo: Mapped[str | None] = mapped_column(Unicode(255))
    intentos_fallidos: Mapped[int] = mapped_column(Integer, default=0)
    bloqueado_hasta: Mapped[datetime | None] = mapped_column(DateTime)
    debe_cambiar_password: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_alta: Mapped[datetime | None] = mapped_column(DateTime)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime)

    @property
    def esta_activo(self) -> bool:
        return self.activo == ACTIVO


class Proposito(StrEnum):
    LOGIN = "LOGIN"
    RECUPERO_PASSWORD = "RECUPERO_PASSWORD"  # noqa: S105 (nombre del propósito, no una contraseña)
    CAMBIO_PASSWORD = "CAMBIO_PASSWORD"  # noqa: S105


class CodigoVerificacion(Base):
    """Código de un solo uso enviado por correo (migración 002_codigos_verificacion)."""

    __tablename__ = "CODIGO_VERIFICACION"

    id_codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("USUARIO.id_usuario"))
    proposito: Mapped[str] = mapped_column(Unicode(30))
    desafio_hash: Mapped[str] = mapped_column(Unicode(64), unique=True)
    codigo_hash: Mapped[str] = mapped_column(Unicode(64))
    canal: Mapped[str] = mapped_column(Unicode(20))
    destino: Mapped[str] = mapped_column(Unicode(255))
    intentos: Mapped[int] = mapped_column(Integer, default=0)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime)
    expira: Mapped[datetime] = mapped_column(DateTime)
    usado_en: Mapped[datetime | None] = mapped_column(DateTime)


class AuditoriaLog(Base):
    __tablename__ = "AUDITORIA_LOG"

    id_log: Mapped[int] = mapped_column(Integer, primary_key=True)
    tabla_afectada: Mapped[str | None] = mapped_column(Unicode(255))
    id_registro_afectado: Mapped[int | None] = mapped_column(Integer)
    accion: Mapped[str | None] = mapped_column(Unicode(255))
    # Columnas de tipo json en SQL Server: se escriben como texto JSON.
    datos_anteriores: Mapped[str | None] = mapped_column(UnicodeText)
    datos_nuevos: Mapped[str | None] = mapped_column(UnicodeText)
    fecha_hora: Mapped[datetime | None] = mapped_column(DateTime)
    usuario: Mapped[str | None] = mapped_column(Unicode(255))
    origen: Mapped[str | None] = mapped_column(Unicode(100))
