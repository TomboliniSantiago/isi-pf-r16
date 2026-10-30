import os

# Antes de importar la app: las pruebas usan SQLite en memoria y no leen la base real.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "secreto-de-pruebas-no-usar-en-produccion"
os.environ["BCRYPT_ROUNDS"] = "4"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, select  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import ACTIVO, AuditoriaLog, Rol, Usuario  # noqa: E402
from app.security import hash_password  # noqa: E402
from app.tiempo import ahora  # noqa: E402

PASSWORD = "Clave1234"


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)

    def _get_db():
        with fabrica() as session:
            yield session

    app.dependency_overrides[get_db] = _get_db
    with fabrica() as session:
        yield session
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def client(db):
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def crear_usuario(db: Session):
    def _crear(email: str, rol: Rol = Rol.CONTADOR, password: str = PASSWORD, **extra) -> Usuario:
        usuario = Usuario(
            nombre_usuario=extra.pop("nombre_usuario", email.split("@")[0]),
            email=email,
            nivel_acceso=rol,
            password_hash=hash_password(password),
            activo=extra.pop("activo", ACTIVO),
            intentos_fallidos=0,
            debe_cambiar_password=extra.pop("debe_cambiar_password", False),
            fecha_alta=ahora(),
            **extra,
        )
        db.add(usuario)
        db.commit()
        return usuario

    return _crear


@pytest.fixture
def login(client):
    def _login(email: str, password: str = PASSWORD) -> dict[str, str]:
        r = client.post("/api/auth/login", json={"email": email, "password": password})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['access_token']}"}

    return _login


@pytest.fixture
def admin(crear_usuario, login):
    usuario = crear_usuario("admin@eugenia.com.ar", Rol.ADMINISTRADOR)
    return usuario, login(usuario.email)


def auditorias(db: Session, accion: str) -> list[AuditoriaLog]:
    db.expire_all()
    return list(db.scalars(select(AuditoriaLog).where(AuditoriaLog.accion == accion)))
