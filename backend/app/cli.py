"""Comandos de administración.

Crear el primer administrador de la aplicación (pide la contraseña por consola):
    python -m app.cli crear-admin --email admin@empresa.com --nombre admin
"""

import argparse
import getpass
import sys

from sqlalchemy import func, or_, select

from app import auditoria
from app.db import get_sessionmaker
from app.models import ACTIVO, Rol, Usuario
from app.security import hash_password, validar_politica
from app.tiempo import ahora


def crear_admin(email: str, nombre: str) -> int:
    email = email.strip().lower()
    password = getpass.getpass("Contraseña: ")
    errores = validar_politica(password)
    if errores:
        print("La contraseña no cumple la política:", *errores, sep="\n  ")
        return 1
    if password != getpass.getpass("Repetir contraseña: "):
        print("Las contraseñas no coinciden.")
        return 1

    with get_sessionmaker()() as db:
        existe = db.scalar(
            select(Usuario.id_usuario).where(
                or_(func.lower(Usuario.email) == email, func.lower(Usuario.nombre_usuario) == nombre.lower())
            )
        )
        if existe:
            print("Ya existe un usuario con ese correo o nombre de usuario.")
            return 1
        usuario = Usuario(
            nombre_usuario=nombre,
            email=email,
            nivel_acceso=Rol.ADMINISTRADOR,
            password_hash=hash_password(password),
            activo=ACTIVO,
            intentos_fallidos=0,
            debe_cambiar_password=False,
            fecha_alta=ahora(),
        )
        db.add(usuario)
        db.flush()
        auditoria.registrar(
            db,
            accion="ALTA",
            tabla="USUARIO",
            id_registro=usuario.id_usuario,
            actor="cli",
            origen="cli",
            despues=auditoria.instantanea_usuario(usuario),
        )
        db.commit()
        print(f"Administrador creado (id {usuario.id_usuario}).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="comando", required=True)
    admin = sub.add_parser("crear-admin", help="Crea un usuario administrador")
    admin.add_argument("--email", required=True)
    admin.add_argument("--nombre", required=True)
    args = parser.parse_args()
    if args.comando == "crear-admin":
        return crear_admin(args.email, args.nombre.strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
