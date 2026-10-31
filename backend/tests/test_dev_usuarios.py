"""CRUD de usuarios sin inicio de sesión (/api/auth/dev/usuarios)."""

import json

from conftest import auditorias

from app.models import INACTIVO, Rol

URL = "/api/auth/dev/usuarios"
NUEVO = {"nombre_usuario": "mperez", "email": "mperez@eugenia.com.ar", "nivel_acceso": "CONTADOR"}


def test_crud_completo_sin_token(client, db):
    r = client.post(URL, json=NUEVO)
    assert r.status_code == 201
    id_usuario = r.json()["usuario"]["id_usuario"]
    assert r.json()["password_temporal"]

    assert client.get(URL).json()[0]["email"] == "mperez@eugenia.com.ar"
    assert client.get(f"{URL}/{id_usuario}").status_code == 200

    r = client.put(f"{URL}/{id_usuario}", json={**NUEVO, "nivel_acceso": "CONSULTA"})
    assert r.status_code == 200
    assert r.json()["nivel_acceso"] == "CONSULTA"

    r = client.delete(f"{URL}/{id_usuario}")
    assert r.status_code == 200
    assert r.json()["activo"] is False

    assert client.post(f"{URL}/{id_usuario}/reactivar").json()["activo"] is True


def test_operaciones_se_auditan_como_sin_sesion(client, db):
    id_usuario = client.post(URL, json=NUEVO).json()["usuario"]["id_usuario"]
    client.put(f"{URL}/{id_usuario}", json={**NUEVO, "nivel_acceso": "CONSULTA"})
    client.delete(f"{URL}/{id_usuario}")

    for accion in ("ALTA", "MODIFICACION", "BAJA"):
        registro = auditorias(db, accion)[0]
        assert registro.usuario == "sin_sesion"
        assert registro.id_registro_afectado == id_usuario
    assert json.loads(auditorias(db, "MODIFICACION")[0].datos_anteriores)["nivel_acceso"] == "CONTADOR"


def test_aplica_las_mismas_validaciones(client, crear_usuario):
    crear_usuario("mperez@eugenia.com.ar")
    assert client.post(URL, json=NUEVO).status_code == 409
    assert client.post(URL, json={**NUEVO, "email": "no-es-correo"}).status_code == 422
    assert client.get(f"{URL}/999").status_code == 404


def test_no_permite_quedarse_sin_administradores(client, crear_usuario):
    admin = crear_usuario("admin@eugenia.com.ar", Rol.ADMINISTRADOR)
    datos = {"nombre_usuario": "admin", "email": admin.email, "nivel_acceso": "CONTADOR"}
    assert client.put(f"{URL}/{admin.id_usuario}", json=datos).status_code == 409
    r = client.delete(f"{URL}/{admin.id_usuario}")
    assert r.status_code == 409
    assert "al menos un administrador" in r.json()["detail"]


def test_baja_de_admin_permitida_si_queda_otro(client, crear_usuario):
    crear_usuario("admin1@eugenia.com.ar", Rol.ADMINISTRADOR)
    admin2 = crear_usuario("admin2@eugenia.com.ar", Rol.ADMINISTRADOR)
    assert client.delete(f"{URL}/{admin2.id_usuario}").status_code == 200


def test_endpoints_con_sesion_siguen_protegidos(client, crear_usuario):
    crear_usuario("inactivo@eugenia.com.ar", activo=INACTIVO)
    assert client.get("/api/usuarios").status_code == 401
