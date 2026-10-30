import jwt
import pytest

from app.config import get_settings
from app.errors import ErrorNegocio
from app.security import (
    crear_token,
    generar_password_temporal,
    hash_password,
    leer_token,
    validar_politica,
    verificar_password,
)


@pytest.mark.parametrize(
    ("password", "esperado"),
    [
        ("Corta1", "al menos 8"),
        ("sinmayuscula1", "mayúscula"),
        ("SINMINUSCULA1", "minúscula"),
        ("SinNumeroAqui", "número"),
        ("Aa1" + "x" * 70, "72 bytes"),
    ],
)
def test_politica_rechaza(password, esperado):
    assert any(esperado in e for e in validar_politica(password))


def test_politica_acepta_password_valida():
    assert validar_politica("Clave1234") == []


def test_hash_no_guarda_texto_plano_y_verifica():
    h = hash_password("Clave1234")
    assert "Clave1234" not in h
    assert verificar_password("Clave1234", h)
    assert not verificar_password("Otra1234", h)


def test_verificar_tolera_hash_invalido_o_vacio():
    assert not verificar_password("Clave1234", None)
    assert not verificar_password("Clave1234", "no-es-bcrypt")


def test_password_temporal_cumple_politica_y_es_aleatoria():
    generadas = {generar_password_temporal() for _ in range(20)}
    assert len(generadas) == 20
    assert all(validar_politica(p) == [] for p in generadas)


def test_token_ida_y_vuelta():
    token, vigencia = crear_token(42)
    assert leer_token(token) == 42
    assert vigencia == get_settings().jwt_expire_minutes * 60


def test_token_vencido_o_adulterado_es_rechazado():
    vencido = jwt.encode({"sub": "1", "exp": 0}, get_settings().jwt_secret, algorithm="HS256")
    with pytest.raises(ErrorNegocio, match="expiró"):
        leer_token(vencido)
    with pytest.raises(ErrorNegocio, match="inválida"):
        leer_token(jwt.encode({"sub": "1", "exp": 9999999999}, "otro-secreto-con-largo-suficiente-xx", "HS256"))
