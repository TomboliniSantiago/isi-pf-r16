"""CUU-018 Gestionar usuarios (alta, modificación, consulta y baja lógica)."""

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import auditoria
from app.errors import ErrorNegocio
from app.models import ACTIVO, INACTIVO, Rol, Usuario
from app.schemas import UsuarioIn
from app.security import generar_password_temporal, hash_password
from app.tiempo import ahora

TABLA = "USUARIO"


def listar(db: Session, buscar: str | None, activo: bool | None, rol: Rol | None) -> list[Usuario]:
    consulta = select(Usuario).order_by(Usuario.nombre_usuario)
    if buscar and buscar.strip():
        patron = f"%{buscar.strip()}%"
        consulta = consulta.where(or_(Usuario.nombre_usuario.ilike(patron), Usuario.email.ilike(patron)))
    if activo is True:
        consulta = consulta.where(Usuario.activo == ACTIVO)
    elif activo is False:
        consulta = consulta.where(or_(Usuario.activo != ACTIVO, Usuario.activo.is_(None)))
    if rol is not None:
        consulta = consulta.where(Usuario.nivel_acceso == rol)
    return list(db.scalars(consulta))


def obtener(db: Session, id_usuario: int) -> Usuario:
    usuario = db.get(Usuario, id_usuario)
    if usuario is None:
        raise ErrorNegocio(404, "El usuario no existe.")
    return usuario


def crear(db: Session, datos: UsuarioIn, actor: Usuario, origen: str | None) -> tuple[Usuario, str]:
    email = datos.email.lower()
    _verificar_duplicados(db, datos.nombre_usuario, email)
    password_temporal = generar_password_temporal()
    usuario = Usuario(
        nombre_usuario=datos.nombre_usuario,
        email=email,
        nivel_acceso=datos.nivel_acceso,
        password_hash=hash_password(password_temporal),
        activo=ACTIVO,
        intentos_fallidos=0,
        debe_cambiar_password=True,
        fecha_alta=ahora(),
    )
    db.add(usuario)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=actor.email,
        origen=origen,
        despues=auditoria.instantanea_usuario(usuario),
    )
    _confirmar(db)
    return usuario, password_temporal


def modificar(db: Session, id_usuario: int, datos: UsuarioIn, actor: Usuario, origen: str | None) -> Usuario:
    usuario = obtener(db, id_usuario)
    email = datos.email.lower()
    if usuario.id_usuario == actor.id_usuario and datos.nivel_acceso != usuario.nivel_acceso:
        raise ErrorNegocio(409, "No puede modificar su propio nivel de acceso.")
    if (
        usuario.nivel_acceso == Rol.ADMINISTRADOR
        and usuario.esta_activo
        and datos.nivel_acceso != Rol.ADMINISTRADOR
        and _administradores_activos(db) <= 1
    ):
        raise ErrorNegocio(409, "Debe existir al menos un administrador activo.")
    _verificar_duplicados(db, datos.nombre_usuario, email, excluir=usuario.id_usuario)

    antes = auditoria.instantanea_usuario(usuario)
    usuario.nombre_usuario = datos.nombre_usuario
    usuario.email = email
    usuario.nivel_acceso = datos.nivel_acceso
    despues = auditoria.instantanea_usuario(usuario)
    if antes != despues:
        auditoria.registrar(
            db,
            accion="MODIFICACION",
            tabla=TABLA,
            id_registro=usuario.id_usuario,
            actor=actor.email,
            origen=origen,
            antes=antes,
            despues=despues,
        )
    _confirmar(db)
    return usuario


def dar_de_baja(db: Session, id_usuario: int, actor: Usuario, origen: str | None) -> Usuario:
    usuario = obtener(db, id_usuario)
    if usuario.id_usuario == actor.id_usuario:
        raise ErrorNegocio(409, "No puede dar de baja su propio usuario.")
    if not usuario.esta_activo:
        raise ErrorNegocio(409, "El usuario ya se encuentra dado de baja.")
    antes = auditoria.instantanea_usuario(usuario)
    usuario.activo = INACTIVO
    auditoria.registrar(
        db,
        accion="BAJA",
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=auditoria.instantanea_usuario(usuario),
    )
    _confirmar(db)
    return usuario


def reactivar(db: Session, id_usuario: int, actor: Usuario, origen: str | None) -> Usuario:
    usuario = obtener(db, id_usuario)
    if usuario.esta_activo:
        raise ErrorNegocio(409, "El usuario ya se encuentra activo.")
    antes = auditoria.instantanea_usuario(usuario)
    usuario.activo = ACTIVO
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    auditoria.registrar(
        db,
        accion="REACTIVACION",
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=auditoria.instantanea_usuario(usuario),
    )
    _confirmar(db)
    return usuario


def restablecer_password(db: Session, id_usuario: int, actor: Usuario, origen: str | None) -> tuple[Usuario, str]:
    """Genera una nueva contraseña temporal y desbloquea la cuenta."""
    usuario = obtener(db, id_usuario)
    if not usuario.esta_activo:
        raise ErrorNegocio(409, "No se puede restablecer la contraseña de un usuario dado de baja.")
    password_temporal = generar_password_temporal()
    usuario.password_hash = hash_password(password_temporal)
    usuario.debe_cambiar_password = True
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    auditoria.registrar(
        db,
        accion="RESTABLECER_PASSWORD",
        tabla=TABLA,
        id_registro=usuario.id_usuario,
        actor=actor.email,
        origen=origen,
        despues={"debe_cambiar_password": True},
    )
    _confirmar(db)
    return usuario, password_temporal


def _verificar_duplicados(db: Session, nombre_usuario: str, email: str, excluir: int | None = None) -> None:
    consulta = select(Usuario).where(
        or_(func.lower(Usuario.email) == email, func.lower(Usuario.nombre_usuario) == nombre_usuario.lower())
    )
    if excluir is not None:
        consulta = consulta.where(Usuario.id_usuario != excluir)
    existente = db.scalars(consulta).first()
    if existente is None:
        return
    if (existente.email or "").lower() == email:
        raise ErrorNegocio(409, f"Ya existe un usuario con el correo {email}.")
    raise ErrorNegocio(409, f"Ya existe un usuario con el nombre de usuario {nombre_usuario}.")


def _administradores_activos(db: Session) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(Usuario)
            .where(Usuario.nivel_acceso == Rol.ADMINISTRADOR, Usuario.activo == ACTIVO)
        )
        or 0
    )


def _confirmar(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:  # carrera contra los índices únicos de email / nombre_usuario
        db.rollback()
        raise ErrorNegocio(409, "Ya existe un usuario con ese correo o nombre de usuario.") from exc
