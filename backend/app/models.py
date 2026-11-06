"""Mapeo de las tablas existentes (esquema base + migraciones 001, 002 y 003)."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

ACTIVO = "S"
INACTIVO = "N"

# PLAN_CUENTA usa otra convención para sus marcas (datos existentes en la base).
CUENTA_SI = "1"
CUENTA_NO = "0"


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


class TipoCuenta(StrEnum):
    ACTIVO = "ACTIVO"
    PASIVO = "PASIVO"
    PATRIMONIO_NETO = "PATRIMONIO_NETO"
    INGRESOS = "INGRESOS"
    GASTOS = "GASTOS"


class Naturaleza(StrEnum):
    DEUDORA = "DEUDORA"
    ACREEDORA = "ACREEDORA"


class ClavePredeterminada(StrEnum):
    """Cuentas que usarán los asientos automáticos de ventas y compras (CUU-001 / CUU-002)."""

    VENTAS = "VENTAS"
    DEUDORES_POR_VENTAS = "DEUDORES_POR_VENTAS"
    IVA_DEBITO_FISCAL = "IVA_DEBITO_FISCAL"
    COMPRAS = "COMPRAS"
    PROVEEDORES = "PROVEEDORES"
    IVA_CREDITO_FISCAL = "IVA_CREDITO_FISCAL"
    RESULTADO_EJERCICIO = "RESULTADO_EJERCICIO"


class PlanCuenta(Base):
    """Cuenta contable (esquema base + migración 003_plan_cuentas)."""

    __tablename__ = "PLAN_CUENTA"

    id_cuenta: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str | None] = mapped_column(Unicode(255), unique=True)
    nombre: Mapped[str | None] = mapped_column(Unicode(255))
    tipo_cuenta: Mapped[str | None] = mapped_column(Unicode(255))
    id_cuenta_padre: Mapped[int | None] = mapped_column(Integer, ForeignKey("PLAN_CUENTA.id_cuenta"))
    imputable: Mapped[str | None] = mapped_column(Unicode(255))
    activo: Mapped[str | None] = mapped_column(Unicode(255))
    naturaleza: Mapped[str | None] = mapped_column(Unicode(20))

    @property
    def esta_activa(self) -> bool:
        return self.activo == CUENTA_SI

    @property
    def es_imputable(self) -> bool:
        return self.imputable == CUENTA_SI


class CuentaPredeterminada(Base):
    __tablename__ = "CUENTA_PREDETERMINADA"

    clave: Mapped[str] = mapped_column(Unicode(40), primary_key=True)
    id_cuenta: Mapped[int | None] = mapped_column(Integer, ForeignKey("PLAN_CUENTA.id_cuenta"))
    fecha_modificacion: Mapped[datetime | None] = mapped_column(DateTime)
    usuario: Mapped[str | None] = mapped_column(Unicode(255))


class AsientoContable(Base):
    """Esquema base. Por ahora solo se lee (movimientos de una cuenta); se gestiona en CUU-003/004."""

    __tablename__ = "ASIENTO_CONTABLE"

    id_asiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_asiento: Mapped[int | None] = mapped_column(Integer)
    fecha: Mapped[date | None] = mapped_column(Date)
    concepto: Mapped[str | None] = mapped_column(Unicode(255))
    tipo_origen: Mapped[str | None] = mapped_column(Unicode(255))
    estado: Mapped[str | None] = mapped_column(Unicode(255))


class DetalleAsiento(Base):
    __tablename__ = "DETALLE_ASIENTO"

    id_detalle_asiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_asiento: Mapped[int] = mapped_column(Integer, ForeignKey("ASIENTO_CONTABLE.id_asiento"))
    id_cuenta: Mapped[int] = mapped_column(Integer, ForeignKey("PLAN_CUENTA.id_cuenta"))
    debe: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    haber: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))


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
