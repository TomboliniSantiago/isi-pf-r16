import pytest
from sqlalchemy.exc import DBAPIError, OperationalError, ProgrammingError

from app.db import get_db
from app.main import app


def _falla(exc: Exception):
    def _get_db():
        raise exc
        yield  # pragma: no cover

    return _get_db


@pytest.mark.parametrize(
    "exc",
    [
        OperationalError("SELECT 1", {}, Exception("Error de tiempo de espera [258]")),
        # Azure SQL serverless reanudándose: pyodbc lo informa como error genérico.
        DBAPIError("SELECT 1", {}, Exception("42000", "Database 'x' is not currently available. (40613)")),
        DBAPIError("SELECT 1", {}, Exception("08S01", "Communication link failure")),
    ],
)
def test_base_no_disponible_responde_503(client, exc):
    app.dependency_overrides[get_db] = _falla(exc)
    r = client.get("/api/auth/dev/usuarios")
    assert r.status_code == 503
    assert "base de datos no está disponible" in r.json()["detail"]


def test_otros_errores_de_base_responden_500(client):
    exc = ProgrammingError("SELECT 1", {}, Exception("42S02", "Invalid object name 'CODIGO_VERIFICACION'."))
    app.dependency_overrides[get_db] = _falla(exc)
    r = client.get("/api/auth/dev/usuarios")
    assert r.status_code == 500
    assert r.json()["detail"] == "No fue posible completar la operación."
