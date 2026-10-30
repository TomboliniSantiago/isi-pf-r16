from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de, usuario_autenticado
from app.models import Usuario
from app.schemas import CambiarPasswordIn, LoginIn, LoginOut, UsuarioOut
from app.security import crear_token
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginOut)
def login(datos: LoginIn, request: Request, db: Session = Depends(get_db)) -> LoginOut:
    usuario = auth_service.autenticar(db, datos.email, datos.password, origen_de(request))
    token, expira_en = crear_token(usuario.id_usuario)
    return LoginOut(access_token=token, expira_en=expira_en, usuario=UsuarioOut.de(usuario))


@router.post("/logout", status_code=204)
def logout(
    request: Request, usuario: Usuario = Depends(usuario_autenticado), db: Session = Depends(get_db)
) -> Response:
    auth_service.cerrar_sesion(db, usuario, origen_de(request))
    return Response(status_code=204)


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(usuario_autenticado)) -> UsuarioOut:
    return UsuarioOut.de(usuario)


@router.post("/cambiar-password", response_model=UsuarioOut)
def cambiar_password(
    datos: CambiarPasswordIn,
    request: Request,
    usuario: Usuario = Depends(usuario_autenticado),
    db: Session = Depends(get_db),
) -> UsuarioOut:
    usuario = auth_service.cambiar_password(
        db, usuario, datos.password_actual, datos.password_nueva, origen_de(request)
    )
    return UsuarioOut.de(usuario)
