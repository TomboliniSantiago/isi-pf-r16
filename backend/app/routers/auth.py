from dataclasses import asdict

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.correo import EnviadorCorreo, get_enviador
from app.db import get_db
from app.deps import origen_de, usuario_autenticado
from app.models import Usuario
from app.schemas import (
    CambiarPasswordIn,
    DesafioOut,
    LoginIn,
    LoginOut,
    RecuperoConfirmarIn,
    RecuperoIn,
    ReenviarCodigoIn,
    UsuarioOut,
    VerificarCodigoIn,
)
from app.security import crear_token
from app.services import auth_service, codigos_service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=DesafioOut)
def login(
    datos: LoginIn,
    request: Request,
    db: Session = Depends(get_db),
    enviador: EnviadorCorreo = Depends(get_enviador),
) -> DesafioOut:
    """Paso 1: correo y contraseña. Si son correctos, envía un código al correo del usuario."""
    desafio = auth_service.iniciar_login(db, datos.email, datos.password, enviador, origen_de(request))
    return DesafioOut(**asdict(desafio))


@router.post("/login/verificar", response_model=LoginOut)
def verificar_login(datos: VerificarCodigoIn, request: Request, db: Session = Depends(get_db)) -> LoginOut:
    """Paso 2: código recibido por correo. Devuelve el token de sesión."""
    usuario = auth_service.completar_login(db, datos.desafio, datos.codigo, origen_de(request))
    token, expira_en = crear_token(usuario.id_usuario)
    return LoginOut(access_token=token, expira_en=expira_en, usuario=UsuarioOut.de(usuario))


@router.post("/codigo/reenviar", response_model=DesafioOut)
def reenviar_codigo(
    datos: ReenviarCodigoIn,
    request: Request,
    db: Session = Depends(get_db),
    enviador: EnviadorCorreo = Depends(get_enviador),
) -> DesafioOut:
    """Envía un nuevo código para un desafío pendiente (login, recupero o cambio de contraseña)."""
    return DesafioOut(**asdict(codigos_service.reenviar(db, datos.desafio, enviador, origen_de(request))))


@router.post("/recuperar-password", response_model=DesafioOut)
def recuperar_password(
    datos: RecuperoIn,
    request: Request,
    db: Session = Depends(get_db),
    enviador: EnviadorCorreo = Depends(get_enviador),
) -> DesafioOut:
    return DesafioOut(**asdict(auth_service.iniciar_recupero(db, datos.email, enviador, origen_de(request))))


@router.post("/recuperar-password/confirmar", status_code=204)
def confirmar_recupero(datos: RecuperoConfirmarIn, request: Request, db: Session = Depends(get_db)) -> Response:
    auth_service.confirmar_recupero(db, datos.desafio, datos.codigo, datos.password_nueva, origen_de(request))
    return Response(status_code=204)


@router.post("/logout", status_code=204)
def logout(
    request: Request, usuario: Usuario = Depends(usuario_autenticado), db: Session = Depends(get_db)
) -> Response:
    auth_service.cerrar_sesion(db, usuario, origen_de(request))
    return Response(status_code=204)


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(usuario_autenticado)) -> UsuarioOut:
    return UsuarioOut.de(usuario)


@router.post("/cambiar-password/codigo", response_model=DesafioOut)
def solicitar_codigo_cambio(
    request: Request,
    usuario: Usuario = Depends(usuario_autenticado),
    db: Session = Depends(get_db),
    enviador: EnviadorCorreo = Depends(get_enviador),
) -> DesafioOut:
    return DesafioOut(**asdict(auth_service.solicitar_codigo_cambio(db, usuario, enviador, origen_de(request))))


@router.post("/cambiar-password", response_model=UsuarioOut)
def cambiar_password(
    datos: CambiarPasswordIn,
    request: Request,
    usuario: Usuario = Depends(usuario_autenticado),
    db: Session = Depends(get_db),
) -> UsuarioOut:
    usuario = auth_service.cambiar_password(
        db,
        usuario,
        datos.password_actual,
        datos.password_nueva,
        datos.desafio,
        datos.codigo,
        origen_de(request),
    )
    return UsuarioOut.de(usuario)
