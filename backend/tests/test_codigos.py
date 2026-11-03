"""Segundo factor por correo (CUU-015 pasos 4-6 y 6.a), recupero (1.a) y cambio de contraseña."""

import json
from datetime import timedelta

import pytest
from conftest import PASSWORD, auditorias

from app.correo import get_enviador
from app.errors import ErrorNegocio
from app.main import app
from app.models import INACTIVO, CodigoVerificacion
from app.tiempo import ahora

EMAIL = "conta@eugenia.com.ar"


def _iniciar_login(client, email=EMAIL, password=PASSWORD) -> str:
    r = client.post("/api/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["desafio"]


def _verificar(client, desafio, codigo):
    return client.post("/api/auth/login/verificar", json={"desafio": desafio, "codigo": codigo})


def _codigo_incorrecto(correcto: str) -> str:
    return "000000" if correcto != "000000" else "111111"


# ---------- Login: paso 6 y camino 6.a ----------


def test_codigo_incorrecto_informa_intentos_restantes(client, db, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    r = _verificar(client, desafio, _codigo_incorrecto(correos.ultimo_codigo()))
    assert r.status_code == 400
    assert "Le quedan 4 intento(s)" in r.json()["detail"]
    assert len(auditorias(db, "CODIGO_INVALIDO")) == 1


def test_codigo_se_invalida_tras_max_intentos(client, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    correcto = correos.ultimo_codigo()
    for _ in range(5):
        r = _verificar(client, desafio, _codigo_incorrecto(correcto))
    assert "Se superó la cantidad de intentos" in r.json()["detail"]
    # Ni el código correcto sirve después.
    assert _verificar(client, desafio, correcto).status_code == 400


def test_codigo_vencido(client, db, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    registro = db.query(CodigoVerificacion).one()
    registro.expira = ahora() - timedelta(seconds=1)
    db.commit()
    r = _verificar(client, desafio, correos.ultimo_codigo())
    assert r.status_code == 400
    assert "venció" in r.json()["detail"]


def test_codigo_de_un_solo_uso(client, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    codigo = correos.ultimo_codigo()
    assert _verificar(client, desafio, codigo).status_code == 200
    assert _verificar(client, desafio, codigo).status_code == 400


def test_nuevo_login_invalida_el_codigo_anterior(client, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio_viejo = _iniciar_login(client)
    codigo_viejo = correos.ultimo_codigo()
    _iniciar_login(client)
    assert _verificar(client, desafio_viejo, codigo_viejo).status_code == 400


def test_codigo_y_desafio_no_se_guardan_en_claro(client, db, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    codigo = correos.ultimo_codigo()
    registro = db.query(CodigoVerificacion).one()
    assert codigo not in registro.codigo_hash
    assert desafio != registro.desafio_hash
    enviado = auditorias(db, "CODIGO_ENVIADO")[0]
    assert codigo not in (enviado.datos_nuevos or "")
    assert json.loads(enviado.datos_nuevos)["destino"] == "c***@eugenia.com.ar"


def test_reenviar_respeta_espera_y_genera_codigo_nuevo(client, db, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    primero = correos.ultimo_codigo()

    r = client.post("/api/auth/codigo/reenviar", json={"desafio": desafio})
    assert r.status_code == 429
    assert "segundo(s)" in r.json()["detail"]

    registro = db.query(CodigoVerificacion).one()
    registro.fecha_creacion = ahora() - timedelta(seconds=61)
    db.commit()
    r = client.post("/api/auth/codigo/reenviar", json={"desafio": desafio})
    assert r.status_code == 200
    nuevo = correos.ultimo_codigo()
    assert len(correos.enviados) == 2
    if nuevo != primero:  # el viejo deja de servir (salvo coincidencia aleatoria)
        assert _verificar(client, desafio, primero).status_code == 400
    assert _verificar(client, desafio, nuevo).status_code == 200


def test_usuario_dado_de_baja_entre_pasos_no_ingresa(client, db, crear_usuario, correos):
    usuario = crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    usuario.activo = INACTIVO
    db.commit()
    assert _verificar(client, desafio, correos.ultimo_codigo()).status_code == 403


def test_falla_de_envio_no_deja_codigo_pendiente(client, db, crear_usuario):
    class CorreoCaido:
        def enviar(self, *_):
            raise ErrorNegocio(503, "No fue posible enviar el código por correo. Intente nuevamente.")

    crear_usuario(EMAIL)
    app.dependency_overrides[get_enviador] = lambda: CorreoCaido()
    r = client.post("/api/auth/login", json={"email": EMAIL, "password": PASSWORD})
    assert r.status_code == 503
    assert db.query(CodigoVerificacion).count() == 0


# ---------- Recupero de contraseña: camino 1.a ----------


def test_recupero_completo(client, db, crear_usuario, correos):
    crear_usuario(EMAIL, bloqueado_hasta=ahora() + timedelta(minutes=10))
    r = client.post("/api/auth/recuperar-password", json={"email": EMAIL})
    assert r.status_code == 200
    desafio = r.json()["desafio"]

    datos = {"desafio": desafio, "codigo": correos.ultimo_codigo(), "password_nueva": "Recuperada99"}
    r = client.post("/api/auth/recuperar-password/confirmar", json=datos)
    assert r.status_code == 204
    assert len(auditorias(db, "RECUPERO_PASSWORD")) == 1

    # 1.a.10: vuelve al login con la nueva contraseña; el recupero desbloqueó la cuenta.
    assert client.post("/api/auth/login", json={"email": EMAIL, "password": "Recuperada99"}).status_code == 200
    assert client.post("/api/auth/login", json={"email": EMAIL, "password": PASSWORD}).status_code == 401


def test_recupero_correo_inexistente(client):
    r = client.post("/api/auth/recuperar-password", json={"email": "nadie@eugenia.com.ar"})
    assert r.status_code == 404
    assert "Contacte al administrador" in r.json()["detail"]


def test_recupero_politica_invalida_no_consume_el_codigo(client, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = client.post("/api/auth/recuperar-password", json={"email": EMAIL}).json()["desafio"]
    codigo = correos.ultimo_codigo()
    url = "/api/auth/recuperar-password/confirmar"

    r = client.post(url, json={"desafio": desafio, "codigo": codigo, "password_nueva": "debil"})
    assert r.status_code == 422  # 1.a.9.a
    assert "mayúscula" in r.json()["detail"]
    r = client.post(url, json={"desafio": desafio, "codigo": codigo, "password_nueva": "Recuperada99"})
    assert r.status_code == 204


def test_codigo_de_login_no_sirve_para_recupero(client, crear_usuario, correos):
    crear_usuario(EMAIL)
    desafio = _iniciar_login(client)
    datos = {"desafio": desafio, "codigo": correos.ultimo_codigo(), "password_nueva": "Recuperada99"}
    assert client.post("/api/auth/recuperar-password/confirmar", json=datos).status_code == 400


# ---------- Cambio de contraseña con sesión ----------


@pytest.fixture
def sesion(crear_usuario, login):
    crear_usuario(EMAIL)
    return login(EMAIL)


def test_cambio_voluntario_exige_codigo(client, sesion):
    datos = {"password_actual": PASSWORD, "password_nueva": "NuevaClave99"}
    r = client.post("/api/auth/cambiar-password", headers=sesion, json=datos)
    assert r.status_code == 400
    assert "código de verificación" in r.json()["detail"]


def test_cambio_voluntario_con_codigo(client, db, sesion, correos):
    r = client.post("/api/auth/cambiar-password/codigo", headers=sesion)
    assert r.status_code == 200
    datos = {
        "password_actual": PASSWORD,
        "password_nueva": "NuevaClave99",
        "desafio": r.json()["desafio"],
        "codigo": correos.ultimo_codigo(),
    }
    assert client.post("/api/auth/cambiar-password", headers=sesion, json=datos).status_code == 200
    assert len(auditorias(db, "CAMBIO_PASSWORD")) == 1


def test_codigo_de_cambio_no_sirve_para_otro_usuario(client, crear_usuario, login, sesion, correos):
    desafio = client.post("/api/auth/cambiar-password/codigo", headers=sesion).json()["desafio"]
    codigo = correos.ultimo_codigo(EMAIL)
    crear_usuario("otro@eugenia.com.ar")
    otro = login("otro@eugenia.com.ar")
    datos = {"password_actual": PASSWORD, "password_nueva": "NuevaClave99", "desafio": desafio, "codigo": codigo}
    assert client.post("/api/auth/cambiar-password", headers=otro, json=datos).status_code == 400
