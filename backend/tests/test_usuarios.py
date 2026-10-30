"""CUU-018 Gestionar usuarios."""

import json

import pytest
from conftest import PASSWORD, auditorias

from app.models import INACTIVO, Rol, Usuario

NUEVO = {"nombre_usuario": "mperez", "email": "MPerez@eugenia.com.ar", "nivel_acceso": "CONTADOR"}


def test_alta_genera_credenciales_iniciales(client, db, admin):
    _, headers = admin
    r = client.post("/api/usuarios", headers=headers, json=NUEVO)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["usuario"]["email"] == "mperez@eugenia.com.ar"
    assert cuerpo["usuario"]["debe_cambiar_password"] is True
    assert cuerpo["usuario"]["activo"] is True

    # La contraseña temporal permite ingresar.
    login = client.post(
        "/api/auth/login", json={"email": "mperez@eugenia.com.ar", "password": cuerpo["password_temporal"]}
    )
    assert login.status_code == 200

    alta = auditorias(db, "ALTA")
    assert len(alta) == 1
    assert alta[0].usuario == "admin@eugenia.com.ar"
    assert json.loads(alta[0].datos_nuevos)["nivel_acceso"] == "CONTADOR"
    assert "password" not in alta[0].datos_nuevos


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"email": "mperez@EUGENIA.com.ar"}, "correo"),
        ({"email": "otro@eugenia.com.ar", "nombre_usuario": "MPEREZ"}, "nombre"),
    ],
)
def test_alta_rechaza_duplicados(client, admin, cambio, mensaje):
    _, headers = admin
    assert client.post("/api/usuarios", headers=headers, json=NUEVO).status_code == 201
    r = client.post("/api/usuarios", headers=headers, json={**NUEVO, **cambio})
    assert r.status_code == 409
    assert mensaje in r.json()["detail"]


@pytest.mark.parametrize(
    "invalido",
    [{"email": "no-es-correo"}, {"nombre_usuario": "ab"}, {"nivel_acceso": "SUPERUSUARIO"}],
)
def test_alta_rechaza_datos_invalidos(client, db, admin, invalido):
    _, headers = admin
    r = client.post("/api/usuarios", headers=headers, json={**NUEVO, **invalido})
    assert r.status_code == 422
    assert r.json()["detail"].startswith("Datos inválidos")
    assert db.query(Usuario).count() == 1  # solo el admin


@pytest.mark.parametrize("rol", [Rol.CONTADOR, Rol.ADMINISTRATIVO, Rol.CONSULTA])
def test_solo_administrador_gestiona_usuarios(client, crear_usuario, login, rol):
    crear_usuario("otro@eugenia.com.ar", rol)
    headers = login("otro@eugenia.com.ar")
    assert client.get("/api/usuarios", headers=headers).status_code == 403
    assert client.post("/api/usuarios", headers=headers, json=NUEVO).status_code == 403


def test_listado_con_filtros(client, admin, crear_usuario):
    _, headers = admin
    crear_usuario("conta@eugenia.com.ar", Rol.CONTADOR)
    crear_usuario("consulta@eugenia.com.ar", Rol.CONSULTA, activo=INACTIVO)

    todos = client.get("/api/usuarios", headers=headers).json()
    assert len(todos) == 3
    activos = client.get("/api/usuarios", headers=headers, params={"activo": True}).json()
    assert {u["email"] for u in activos} == {"admin@eugenia.com.ar", "conta@eugenia.com.ar"}
    por_rol = client.get("/api/usuarios", headers=headers, params={"rol": "CONSULTA"}).json()
    assert [u["email"] for u in por_rol] == ["consulta@eugenia.com.ar"]
    por_texto = client.get("/api/usuarios", headers=headers, params={"buscar": "CONTA"}).json()
    assert [u["email"] for u in por_texto] == ["conta@eugenia.com.ar"]


def test_consulta_de_usuario_inexistente(client, admin):
    _, headers = admin
    assert client.get("/api/usuarios/999", headers=headers).status_code == 404


def test_modificacion_audita_antes_y_despues(client, db, admin, crear_usuario):
    _, headers = admin
    usuario = crear_usuario("conta@eugenia.com.ar", Rol.CONTADOR)
    datos = {"nombre_usuario": "contador1", "email": "conta@eugenia.com.ar", "nivel_acceso": "CONSULTA"}
    r = client.put(f"/api/usuarios/{usuario.id_usuario}", headers=headers, json=datos)
    assert r.status_code == 200
    assert r.json()["nivel_acceso"] == "CONSULTA"

    registro = auditorias(db, "MODIFICACION")[0]
    assert json.loads(registro.datos_anteriores)["nivel_acceso"] == "CONTADOR"
    assert json.loads(registro.datos_nuevos)["nivel_acceso"] == "CONSULTA"
    assert registro.id_registro_afectado == usuario.id_usuario


def test_cambio_de_rol_aplica_de_inmediato(client, admin, crear_usuario, login):
    _, headers = admin
    usuario = crear_usuario("otro@eugenia.com.ar", Rol.ADMINISTRADOR)
    headers_otro = login(usuario.email)
    assert client.get("/api/usuarios", headers=headers_otro).status_code == 200
    datos = {"nombre_usuario": "otro", "email": usuario.email, "nivel_acceso": "CONSULTA"}
    assert client.put(f"/api/usuarios/{usuario.id_usuario}", headers=headers, json=datos).status_code == 200
    assert client.get("/api/usuarios", headers=headers_otro).status_code == 403


def test_administrador_no_cambia_su_propio_rol(client, admin):
    usuario, headers = admin
    datos = {"nombre_usuario": "admin", "email": usuario.email, "nivel_acceso": "CONTADOR"}
    r = client.put(f"/api/usuarios/{usuario.id_usuario}", headers=headers, json=datos)
    assert r.status_code == 409


def test_modificacion_rechaza_correo_de_otro_usuario(client, admin, crear_usuario):
    _, headers = admin
    usuario = crear_usuario("conta@eugenia.com.ar")
    datos = {"nombre_usuario": "conta", "email": "admin@eugenia.com.ar", "nivel_acceso": "CONTADOR"}
    assert client.put(f"/api/usuarios/{usuario.id_usuario}", headers=headers, json=datos).status_code == 409


def test_baja_logica_revoca_acceso(client, db, admin, crear_usuario, login):
    _, headers = admin
    usuario = crear_usuario("conta@eugenia.com.ar")
    headers_conta = login(usuario.email)

    r = client.post(f"/api/usuarios/{usuario.id_usuario}/baja", headers=headers)
    assert r.status_code == 200
    assert r.json()["activo"] is False
    db.refresh(usuario)
    assert usuario.activo == INACTIVO  # el registro se conserva
    assert len(auditorias(db, "BAJA")) == 1

    assert client.get("/api/auth/me", headers=headers_conta).status_code == 401
    assert client.post("/api/auth/login", json={"email": usuario.email, "password": PASSWORD}).status_code == 403
    assert client.post(f"/api/usuarios/{usuario.id_usuario}/baja", headers=headers).status_code == 409


def test_administrador_no_se_da_de_baja_a_si_mismo(client, admin):
    usuario, headers = admin
    assert client.post(f"/api/usuarios/{usuario.id_usuario}/baja", headers=headers).status_code == 409


def test_reactivar_usuario(client, db, admin, crear_usuario):
    _, headers = admin
    usuario = crear_usuario("conta@eugenia.com.ar", activo=INACTIVO)
    r = client.post(f"/api/usuarios/{usuario.id_usuario}/reactivar", headers=headers)
    assert r.status_code == 200
    assert r.json()["activo"] is True
    assert len(auditorias(db, "REACTIVACION")) == 1
    assert client.post("/api/auth/login", json={"email": usuario.email, "password": PASSWORD}).status_code == 200


def test_restablecer_password_desbloquea(client, db, admin, crear_usuario):
    _, headers = admin
    usuario = crear_usuario("conta@eugenia.com.ar")
    for _ in range(3):
        client.post("/api/auth/login", json={"email": usuario.email, "password": "Incorrecta1"})

    r = client.post(f"/api/usuarios/{usuario.id_usuario}/restablecer-password", headers=headers)
    assert r.status_code == 200
    temporal = r.json()["password_temporal"]
    assert r.json()["usuario"]["debe_cambiar_password"] is True
    login = client.post("/api/auth/login", json={"email": usuario.email, "password": temporal})
    assert login.status_code == 200
    assert temporal not in (auditorias(db, "RESTABLECER_PASSWORD")[0].datos_nuevos or "")
