"""CUU-015 Iniciar sesión."""

import json
from datetime import timedelta

from conftest import PASSWORD, auditorias

from app.models import INACTIVO, Rol
from app.tiempo import ahora


def _login(client, email, password=PASSWORD):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def test_login_exitoso(client, db, crear_usuario):
    usuario = crear_usuario("conta@eugenia.com.ar")
    r = _login(client, "Conta@Eugenia.com.ar")  # el correo no distingue mayúsculas
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["token_type"] == "bearer"
    assert cuerpo["usuario"]["nivel_acceso"] == Rol.CONTADOR
    assert "password_hash" not in cuerpo["usuario"]
    db.refresh(usuario)
    assert usuario.ultimo_acceso is not None
    assert len(auditorias(db, "LOGIN_OK")) == 1


def test_correo_no_registrado(client, db):
    r = _login(client, "nadie@eugenia.com.ar")
    assert r.status_code == 401
    assert "Contacte al administrador" in r.json()["detail"]
    assert len(auditorias(db, "LOGIN_FALLIDO")) == 1


def test_password_incorrecta_informa_intentos_restantes(client, db, crear_usuario):
    usuario = crear_usuario("conta@eugenia.com.ar")
    r = _login(client, usuario.email, "Incorrecta1")
    assert r.status_code == 401
    assert "Le quedan 2 intento(s)" in r.json()["detail"]
    db.refresh(usuario)
    assert usuario.intentos_fallidos == 1


def test_tercer_intento_fallido_bloquea_temporalmente(client, db, crear_usuario):
    usuario = crear_usuario("conta@eugenia.com.ar")
    _login(client, usuario.email, "Incorrecta1")
    _login(client, usuario.email, "Incorrecta1")
    r = _login(client, usuario.email, "Incorrecta1")
    assert r.status_code == 423
    assert "15 minuto(s)" in r.json()["detail"]
    db.refresh(usuario)
    assert usuario.bloqueado_hasta is not None
    assert len(auditorias(db, "BLOQUEO")) == 1

    # Bloqueada, ni siquiera la contraseña correcta concede acceso.
    assert _login(client, usuario.email).status_code == 423


def test_login_exitoso_reinicia_intentos(client, db, crear_usuario):
    usuario = crear_usuario("conta@eugenia.com.ar")
    _login(client, usuario.email, "Incorrecta1")
    _login(client, usuario.email, "Incorrecta1")
    assert _login(client, usuario.email).status_code == 200
    db.refresh(usuario)
    assert usuario.intentos_fallidos == 0
    # Tras reiniciar, un nuevo fallo no bloquea.
    assert _login(client, usuario.email, "Incorrecta1").status_code == 401


def test_bloqueo_vencido_permite_ingresar(client, db, crear_usuario):
    crear_usuario("conta@eugenia.com.ar", bloqueado_hasta=ahora() - timedelta(minutes=1))
    assert _login(client, "conta@eugenia.com.ar").status_code == 200


def test_usuario_dado_de_baja_no_ingresa(client, crear_usuario):
    crear_usuario("conta@eugenia.com.ar", activo=INACTIVO)
    r = _login(client, "conta@eugenia.com.ar")
    assert r.status_code == 403
    assert "deshabilitada" in r.json()["detail"]


def test_endpoints_protegidos_exigen_token(client):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/usuarios").status_code == 401
    r = client.get("/api/auth/me", headers={"Authorization": "Bearer basura"})
    assert r.status_code == 401


def test_me_devuelve_usuario_actual(client, crear_usuario, login):
    crear_usuario("conta@eugenia.com.ar")
    r = client.get("/api/auth/me", headers=login("conta@eugenia.com.ar"))
    assert r.status_code == 200
    assert r.json()["email"] == "conta@eugenia.com.ar"


def test_logout_queda_auditado(client, db, crear_usuario, login):
    crear_usuario("conta@eugenia.com.ar")
    r = client.post("/api/auth/logout", headers=login("conta@eugenia.com.ar"))
    assert r.status_code == 204
    assert len(auditorias(db, "LOGOUT")) == 1


def test_password_temporal_obliga_a_cambiarla(client, db, crear_usuario, login):
    crear_usuario("nuevo@eugenia.com.ar", Rol.ADMINISTRADOR, debe_cambiar_password=True)
    headers = login("nuevo@eugenia.com.ar")
    r = client.get("/api/usuarios", headers=headers)
    assert r.status_code == 403
    assert "cambiar su contraseña" in r.json()["detail"]

    r = client.post(
        "/api/auth/cambiar-password",
        headers=headers,
        json={"password_actual": PASSWORD, "password_nueva": "NuevaClave99"},
    )
    assert r.status_code == 200
    assert r.json()["debe_cambiar_password"] is False
    assert client.get("/api/usuarios", headers=headers).status_code == 200
    assert _login(client, "nuevo@eugenia.com.ar", "NuevaClave99").status_code == 200

    registro = auditorias(db, "CAMBIO_PASSWORD")[0]
    assert "NuevaClave99" not in json.dumps([registro.datos_anteriores, registro.datos_nuevos])


def test_cambiar_password_valida_actual_y_politica(client, crear_usuario, login):
    crear_usuario("conta@eugenia.com.ar")
    headers = login("conta@eugenia.com.ar")
    url = "/api/auth/cambiar-password"

    r = client.post(url, headers=headers, json={"password_actual": "Mal12345", "password_nueva": "NuevaClave99"})
    assert r.status_code == 400

    r = client.post(url, headers=headers, json={"password_actual": PASSWORD, "password_nueva": "debil"})
    assert r.status_code == 422
    assert "mayúscula" in r.json()["detail"]

    r = client.post(url, headers=headers, json={"password_actual": PASSWORD, "password_nueva": PASSWORD})
    assert r.status_code == 422
    assert "distinta" in r.json()["detail"]
