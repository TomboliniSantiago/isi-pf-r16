"""CUU-006 Consultar Libro Mayor."""

from decimal import Decimal

import pytest

from app.models import PlanCuenta, Rol

URL = "/api/libro-mayor"


@pytest.fixture
def cuentas(db):
    """Rubro 1.1.1 Caja y Bancos (Caja, Banco) y Capital."""

    def cuenta(codigo, nombre, tipo, padre=None, imputable="1"):
        c = PlanCuenta(
            codigo=codigo,
            nombre=nombre,
            tipo_cuenta=tipo,
            id_cuenta_padre=padre,
            imputable=imputable,
            activo="1",
            naturaleza="DEUDORA",
        )
        db.add(c)
        db.flush()
        return c.id_cuenta

    rubro = cuenta("1.1.1", "Caja y Bancos", "ACTIVO", imputable="0")
    ids = {
        "rubro": rubro,
        "caja": cuenta("1.1.1.01", "Caja", "ACTIVO", rubro),
        "banco": cuenta("1.1.1.03", "Banco", "ACTIVO", rubro),
        "capital": cuenta("3.1", "Capital Social", "PATRIMONIO_NETO"),
    }
    db.commit()
    return ids


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


@pytest.fixture
def asentar(client, contador, cuentas):
    def _asentar(fecha, debe, haber, importe, confirmar=True, concepto="Movimiento"):
        r = client.post(
            "/api/asientos",
            headers=contador,
            json={
                "fecha": fecha,
                "concepto": concepto,
                "lineas": [
                    {"id_cuenta": cuentas[debe], "debe": importe, "haber": "0"},
                    {"id_cuenta": cuentas[haber], "debe": "0", "haber": importe},
                ],
                "confirmar": confirmar,
            },
        )
        assert r.status_code == 201, r.text
        return r.json()

    return _asentar


def _mayor(client, headers, id_cuenta, **params):
    r = client.get(URL, headers=headers, params={"id_cuenta": id_cuenta, **params})
    assert r.status_code == 200, r.text
    return r.json()


def test_saldo_inicial_movimientos_y_saldo_final(client, contador, cuentas, asentar):
    asentar("2026-09-15", "caja", "capital", "1000.00")  # antes del período: saldo inicial
    asentar("2026-10-05", "caja", "capital", "500.00")
    asentar("2026-10-20", "banco", "caja", "300.00")
    asentar("2026-11-02", "caja", "capital", "999.00")  # después del período

    mayor = _mayor(client, contador, cuentas["caja"], desde="2026-10-01", hasta="2026-10-31")
    caja = mayor["cuentas"][0]
    assert Decimal(caja["saldo_inicial"]) == Decimal("1000.00")
    assert [Decimal(m["debe"]) for m in caja["movimientos"]] == [Decimal("500.00"), Decimal("0.00")]
    assert [Decimal(m["haber"]) for m in caja["movimientos"]] == [Decimal("0.00"), Decimal("300.00")]
    assert [Decimal(m["saldo"]) for m in caja["movimientos"]] == [Decimal("1500.00"), Decimal("1200.00")]
    assert Decimal(caja["total_debe"]) == Decimal("500.00") and Decimal(caja["total_haber"]) == Decimal("300.00")
    assert Decimal(caja["saldo_final"]) == Decimal("1200.00")
    assert caja["movimientos"][0]["numero_asiento"] == 2 and caja["movimientos"][0]["tipo_origen"] == "MANUAL"


def test_saldo_acreedor_es_negativo(client, contador, cuentas, asentar):
    asentar("2026-10-05", "caja", "capital", "500.00")
    capital = _mayor(client, contador, cuentas["capital"])["cuentas"][0]
    assert Decimal(capital["saldo_final"]) == Decimal("-500.00")


def test_sin_movimientos_en_el_periodo_informa_saldo_arrastrado(client, contador, cuentas, asentar):  # 2.a
    asentar("2026-09-15", "caja", "capital", "1000.00")
    caja = _mayor(client, contador, cuentas["caja"], desde="2026-10-01")["cuentas"][0]
    assert caja["movimientos"] == []
    assert Decimal(caja["saldo_inicial"]) == Decimal(caja["saldo_final"]) == Decimal("1000.00")


def test_cuenta_sin_ningun_movimiento(client, contador, cuentas):
    caja = _mayor(client, contador, cuentas["caja"])["cuentas"][0]
    assert caja["movimientos"] == [] and Decimal(caja["saldo_final"]) == 0


def test_los_borradores_no_tienen_efecto(client, contador, cuentas, asentar):
    asentar("2026-10-05", "caja", "capital", "500.00", confirmar=False)
    caja = _mayor(client, contador, cuentas["caja"])["cuentas"][0]
    assert caja["movimientos"] == [] and Decimal(caja["saldo_final"]) == 0


def test_anulacion_muestra_asiento_y_contra_asiento(client, contador, cuentas, asentar):
    asiento = asentar("2026-10-05", "caja", "capital", "500.00")
    client.post(f"/api/asientos/{asiento['id_asiento']}/anular", headers=contador)
    caja = _mayor(client, contador, cuentas["caja"])["cuentas"][0]
    assert [m["tipo_origen"] for m in caja["movimientos"]] == ["MANUAL", "REVERSION"]
    assert caja["movimientos"][0]["estado"] == "ANULADO"
    assert Decimal(caja["saldo_final"]) == 0


def test_rubro_reune_sus_cuentas_imputables(client, contador, cuentas, asentar):
    asentar("2026-10-05", "caja", "capital", "500.00")
    asentar("2026-10-06", "banco", "capital", "200.00")
    mayor = _mayor(client, contador, cuentas["rubro"])
    assert mayor["imputable"] is False
    assert [c["codigo"] for c in mayor["cuentas"]] == ["1.1.1.01", "1.1.1.03"]
    assert Decimal(mayor["saldo_final"]) == Decimal("700.00")
    assert Decimal(mayor["total_debe"]) == Decimal("700.00")


def test_rubro_omite_cuentas_sin_saldo_ni_movimientos(client, contador, cuentas, asentar):
    asentar("2026-10-05", "caja", "capital", "500.00")
    assert [c["codigo"] for c in _mayor(client, contador, cuentas["rubro"])["cuentas"]] == ["1.1.1.01"]


def test_periodo_invalido(client, contador, cuentas):
    r = client.get(
        URL, headers=contador, params={"id_cuenta": cuentas["caja"], "desde": "2026-11-01", "hasta": "2026-10-01"}
    )
    assert r.status_code == 422


def test_cuenta_inexistente(client, contador, cuentas):
    assert client.get(URL, headers=contador, params={"id_cuenta": 999}).status_code == 404


def test_rol_consulta_puede_consultar(client, crear_usuario, login, cuentas):
    crear_usuario("consulta@eugenia.com.ar", Rol.CONSULTA)
    assert _mayor(client, login("consulta@eugenia.com.ar"), cuentas["caja"])["cuentas"]


def test_sin_sesion(client, cuentas):
    assert client.get(URL, params={"id_cuenta": cuentas["caja"]}).status_code == 401
