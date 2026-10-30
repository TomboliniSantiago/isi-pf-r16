"""Mapeo de las tablas existentes (esquema base + migración 001_seguridad_usuarios)."""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, Integer, Unicode, UnicodeText
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
