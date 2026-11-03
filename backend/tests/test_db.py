import pytest

from app.db import conectar_con_reintentos

REANUDANDO = Exception("HY000", "Database 'x' is not currently available. (40613)")


def _conexion(fallas: list[Exception]):
    llamadas = []

    def conectar():
        llamadas.append(1)
        if fallas:
            raise fallas.pop(0)
        return "conexion"

    return conectar, llamadas


def test_reintenta_mientras_la_base_se_reanuda():
    conectar, llamadas = _conexion([REANUDANDO, REANUDANDO])
    esperas = []
    assert conectar_con_reintentos(conectar, intentos=6, espera=10, dormir=esperas.append) == "conexion"
    assert len(llamadas) == 3
    assert esperas == [10, 10]


def test_se_rinde_al_agotar_los_intentos():
    conectar, llamadas = _conexion([REANUDANDO] * 5)
    with pytest.raises(Exception, match="40613"):
        conectar_con_reintentos(conectar, intentos=3, espera=10, dormir=lambda _: None)
    assert len(llamadas) == 3


def test_otros_errores_no_se_reintentan():
    conectar, llamadas = _conexion([Exception("28000", "Login failed for user 'APPusr'. (18456)")])
    with pytest.raises(Exception, match="18456"):
        conectar_con_reintentos(conectar, intentos=6, espera=10, dormir=lambda _: None)
    assert len(llamadas) == 1
