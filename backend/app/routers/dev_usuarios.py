"""CRUD de usuarios SIN inicio de sesión, para desarrollo.

ATENCIÓN: cualquiera que llegue a la API puede crear, modificar y dar de baja usuarios,
incluidos administradores. Quitar este router (y su include en main.py) antes de exponer
la aplicación fuera del entorno local. Las operaciones se auditan con usuario "sin_sesion".
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de
from app.models import Rol
from app.schemas import UsuarioConPasswordOut, UsuarioIn, UsuarioOut
from app.services import usuarios_service

router = APIRouter(prefix="/api/auth/dev/usuarios", tags=["Usuarios sin sesión (desarrollo)"])


@router.get("", response_model=list[UsuarioOut])
def listar(
    buscar: str | None = Query(None, max_length=100),
    activo: bool | None = None,
    rol: Rol | None = None,
    db: Session = Depends(get_db),
) -> list[UsuarioOut]:
    return [UsuarioOut.de(u) for u in usuarios_service.listar(db, buscar, activo, rol)]


@router.get("/{id_usuario}", response_model=UsuarioOut)
def obtener(id_usuario: int, db: Session = Depends(get_db)) -> UsuarioOut:
    return UsuarioOut.de(usuarios_service.obtener(db, id_usuario))


@router.post("", response_model=UsuarioConPasswordOut, status_code=201)
def crear(datos: UsuarioIn, request: Request, db: Session = Depends(get_db)) -> UsuarioConPasswordOut:
    usuario, password = usuarios_service.crear(db, datos, None, origen_de(request))
    return UsuarioConPasswordOut(usuario=UsuarioOut.de(usuario), password_temporal=password)


@router.put("/{id_usuario}", response_model=UsuarioOut)
def modificar(id_usuario: int, datos: UsuarioIn, request: Request, db: Session = Depends(get_db)) -> UsuarioOut:
    return UsuarioOut.de(usuarios_service.modificar(db, id_usuario, datos, None, origen_de(request)))


@router.delete("/{id_usuario}", response_model=UsuarioOut)
def dar_de_baja(id_usuario: int, request: Request, db: Session = Depends(get_db)) -> UsuarioOut:
    """Baja lógica: el registro se conserva con activo = 'N'."""
    return UsuarioOut.de(usuarios_service.dar_de_baja(db, id_usuario, None, origen_de(request)))


@router.post("/{id_usuario}/reactivar", response_model=UsuarioOut)
def reactivar(id_usuario: int, request: Request, db: Session = Depends(get_db)) -> UsuarioOut:
    return UsuarioOut.de(usuarios_service.reactivar(db, id_usuario, None, origen_de(request)))
