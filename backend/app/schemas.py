from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

from app.models import Rol, Usuario
from app.tiempo import a_utc, ahora

NombreUsuario = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=100)]


class LoginIn(BaseModel):
    # Texto libre: un correo mal formado se informa igual que uno inexistente (CUU-015 2.a).
    email: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
    password: str = Field(min_length=1, max_length=128)


class CambiarPasswordIn(BaseModel):
    password_actual: str = Field(min_length=1, max_length=128)
    password_nueva: str = Field(min_length=1, max_length=128)


class UsuarioIn(BaseModel):
    nombre_usuario: NombreUsuario
    email: EmailStr = Field(max_length=255)
    nivel_acceso: Rol


class UsuarioOut(BaseModel):
    id_usuario: int
    nombre_usuario: str | None
    email: str | None
    nivel_acceso: str | None
    activo: bool
    bloqueado: bool
    debe_cambiar_password: bool
    fecha_alta: datetime | None
    ultimo_acceso: datetime | None

    @classmethod
    def de(cls, usuario: Usuario) -> "UsuarioOut":
        return cls(
            id_usuario=usuario.id_usuario,
            nombre_usuario=usuario.nombre_usuario,
            email=usuario.email,
            nivel_acceso=usuario.nivel_acceso,
            activo=usuario.esta_activo,
            bloqueado=bool(usuario.bloqueado_hasta and usuario.bloqueado_hasta > ahora()),
            debe_cambiar_password=usuario.debe_cambiar_password,
            fecha_alta=a_utc(usuario.fecha_alta),
            ultimo_acceso=a_utc(usuario.ultimo_acceso),
        )


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105 (tipo de token, no una contraseña)
    expira_en: int
    usuario: UsuarioOut


class UsuarioConPasswordOut(BaseModel):
    """Respuesta de alta o restablecimiento: la contraseña temporal se muestra una sola vez."""

    usuario: UsuarioOut
    password_temporal: str
