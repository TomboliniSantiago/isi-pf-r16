"""CUU-003 Gestionar Libro Diario y CUU-004 Registrar asiento manual."""

from decimal import Decimal

import pytest
from conftest import auditorias

from app.models import AsientoContable, DetalleAsiento, PlanCuenta, Rol

URL = "/api/asientos"


@pytest.fixture
def cuentas(db):
    """Rubro 1.1.1 con Caja y Banco (imputables), Capital, y una cuenta dada de baja."""

    def cuenta(codigo, nombre, tipo, imputable="1", activo="1"):
        c = PlanCuenta(
            codigo=codigo, nombre=nombre, tipo_cuenta=tipo, imputable=imputable, activo=activo, naturaleza="DEUDORA"
        )
        db.add(c)
        db.flush()
        return c.id_cuenta

    ids = {
        "rubro": cuenta("1.1.1", "Caja y Bancos", "ACTIVO", imputable="0"),
        "caja": cuenta("1.1.1.01", "Caja", "ACTIVO"),
        "banco": cuenta("1.1.1.03", "Banco", "ACTIVO"),
        "capital": cuenta("3.1", "Capital Social", "PATRIMONIO_NETO"),
        "baja": cuenta("1.1.1.04", "Banco B", "ACTIVO", activo="0"),
    }
    db.commit()
    return ids


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


def _asiento(cuentas, debe="caja", haber="capital", importe="1000.00", confirmar=True, **extra):
    return {
        "fecha": "2026-11-10",
        "concepto": "Aporte de capital",
        "lineas": [
            {"id_cuenta": cuentas[debe], "debe": importe, "haber": "0"},
            {"id_cuenta": cuentas[haber], "debe": "0", "haber": importe},
        ],
        "confirmar": confirmar,
        **extra,
    }


@pytest.fixture
def asentado(client, contador, cuentas):
    r = client.post(URL, headers=contador, json=_asiento(cuentas))
    assert r.status_code == 201, r.text
    return r.json()


# ---------- Alta (CUU-004) ----------


def test_alta_confirmada_numera_y_audita(client, db, asentado):
    assert asentado["estado"] == "ASENTADO" and asentado["numero_asiento"] == 1
    assert asentado["tipo_origen"] == "MANUAL"
    assert Decimal(asentado["total_debe"]) == Decimal(asentado["total_haber"]) == Decimal("1000.00")
    assert [linea["codigo"] for linea in asentado["lineas"]] == ["1.1.1.01", "3.1"]
    assert len(auditorias(db, "ALTA")) == 1


def test_numeracion_correlativa(client, contador, cuentas, asentado):
    segundo = client.post(URL, headers=contador, json=_asiento(cuentas, debe="banco")).json()
    assert segundo["numero_asiento"] == 2


def test_asiento_desbalanceado(client, db, contador, cuentas):  # 3.a
    datos = _asiento(cuentas)
    datos["lineas"][1]["haber"] = "900.00"
    r = client.post(URL, headers=contador, json=datos)
    assert r.status_code == 422
    assert "diferencia 100.00" in r.json()["detail"]
    assert db.query(AsientoContable).count() == 0


@pytest.mark.parametrize(
    ("linea", "mensaje"),
    [
        ({"debe": "100", "haber": "100"}, "no en ambos"),
        ({"debe": "0", "haber": "0"}, "mayor a cero"),
    ],
)
def test_importe_invalido_indica_la_linea(client, contador, cuentas, linea, mensaje):  # 2.a
    datos = _asiento(cuentas)
    datos["lineas"][0].update(linea)
    r = client.post(URL, headers=contador, json=datos)
    assert r.status_code == 422 and r.json()["detail"].startswith("Línea 1") and mensaje in r.json()["detail"]


def test_importe_negativo_o_con_mas_de_dos_decimales(client, contador, cuentas):
    for importe in ("-10", "10.123"):
        datos = _asiento(cuentas)
        datos["lineas"][0]["debe"] = importe
        assert client.post(URL, headers=contador, json=datos).status_code == 422


@pytest.mark.parametrize(("cuenta", "mensaje"), [("rubro", "es un rubro"), ("baja", "dada de baja")])
def test_cuenta_no_vigente_o_no_imputable(client, contador, cuentas, cuenta, mensaje):
    r = client.post(URL, headers=contador, json=_asiento(cuentas, debe=cuenta))
    assert r.status_code == 422 and mensaje in r.json()["detail"]


def test_totales_sin_guardar(client, db, contador, cuentas):  # pasos 2-3
    datos = _asiento(cuentas)
    datos["lineas"][1]["haber"] = "400.00"
    r = client.post(f"{URL}/totales", headers=contador, json=datos["lineas"])
    assert r.status_code == 200
    assert r.json() == {"total_debe": "1000.00", "total_haber": "400.00", "diferencia": "600.00", "balanceado": False}
    assert db.query(AsientoContable).count() == 0


# ---------- Borradores ----------


def test_borrador_sin_numero_y_confirmacion(client, db, contador, cuentas):
    borrador = client.post(URL, headers=contador, json=_asiento(cuentas, confirmar=False)).json()
    assert borrador["estado"] == "BORRADOR" and borrador["numero_asiento"] is None

    r = client.post(f"{URL}/{borrador['id_asiento']}/confirmar", headers=contador)
    assert r.status_code == 200
    assert r.json()["estado"] == "ASENTADO" and r.json()["numero_asiento"] == 1
    assert len(auditorias(db, "CONFIRMACION")) == 1
    assert client.post(f"{URL}/{borrador['id_asiento']}/confirmar", headers=contador).status_code == 409


def test_borrador_desbalanceado_no_se_confirma(client, contador, cuentas):
    datos = _asiento(cuentas, confirmar=False)
    datos["lineas"][1]["haber"] = "10.00"
    borrador = client.post(URL, headers=contador, json=datos).json()
    r = client.post(f"{URL}/{borrador['id_asiento']}/confirmar", headers=contador)
    assert r.status_code == 422 and "no está balanceado" in r.json()["detail"]


# ---------- Anulación (CUU-003 3.b) ----------


def test_anular_asentado_genera_contra_asiento(client, db, contador, asentado):
    r = client.post(f"{URL}/{asentado['id_asiento']}/anular", headers=contador)
    assert r.status_code == 200
    contra = r.json()
    assert contra["tipo_origen"] == "REVERSION" and contra["estado"] == "ASENTADO"
    assert contra["numero_asiento"] == 2 and contra["revierte_a"] == 1
    # Debe y Haber invertidos.
    assert [(linea["codigo"], linea["debe"], linea["haber"]) for linea in contra["lineas"]] == [
        ("1.1.1.01", "0.00", "1000.00"),
        ("3.1", "1000.00", "0.00"),
    ]
    original = client.get(f"{URL}/{asentado['id_asiento']}", headers=contador).json()
    assert original["estado"] == "ANULADO" and original["revertido_por"] == 2
    # No se borra ni se sobrescribe nada: el original conserva sus líneas.
    assert db.query(DetalleAsiento).filter_by(id_asiento=asentado["id_asiento"]).count() == 2
    assert len(auditorias(db, "REVERSION")) == 1


def test_anular_borrador_lo_descarta_sin_contra_asiento(client, db, contador, cuentas):
    borrador = client.post(URL, headers=contador, json=_asiento(cuentas, confirmar=False)).json()
    r = client.post(f"{URL}/{borrador['id_asiento']}/anular", headers=contador)
    assert r.json()["estado"] == "ANULADO" and r.json()["numero_asiento"] is None
    assert db.query(AsientoContable).count() == 1


@pytest.mark.parametrize("origen", ["VENTA", "COMPRA", "REVERSION"])
def test_asientos_no_manuales_no_se_anulan_ni_modifican(client, db, contador, cuentas, asentado, origen):
    asiento = db.get(AsientoContable, asentado["id_asiento"])
    asiento.tipo_origen = origen
    db.commit()
    assert client.post(f"{URL}/{asentado['id_asiento']}/anular", headers=contador).status_code == 409
    assert client.put(f"{URL}/{asentado['id_asiento']}", headers=contador, json=_asiento(cuentas)).status_code == 409


def test_no_se_anula_dos_veces(client, contador, asentado):
    client.post(f"{URL}/{asentado['id_asiento']}/anular", headers=contador)
    r = client.post(f"{URL}/{asentado['id_asiento']}/anular", headers=contador)
    assert r.status_code == 409 and "ya está anulado" in r.json()["detail"]


# ---------- Modificación (CUU-003 3.a) ----------


def test_modificar_asentado_revierte_y_crea_nuevo(client, db, contador, cuentas, asentado):
    r = client.put(
        f"{URL}/{asentado['id_asiento']}", headers=contador, json=_asiento(cuentas, debe="banco", importe="1500.00")
    )
    assert r.status_code == 200
    nuevo = r.json()
    assert nuevo["estado"] == "ASENTADO" and nuevo["numero_asiento"] == 3  # 2 es el contra-asiento
    assert nuevo["referencia"] == "Rectifica el asiento N° 1"
    assert Decimal(nuevo["total_debe"]) == Decimal("1500.00")
    original = client.get(f"{URL}/{asentado['id_asiento']}", headers=contador).json()
    assert original["estado"] == "ANULADO" and original["revertido_por"] == 2
    assert len(auditorias(db, "MODIFICACION")) == 1


def test_modificacion_desbalanceada_no_anula_el_original(client, contador, cuentas, asentado):  # 3.a.2
    datos = _asiento(cuentas)
    datos["lineas"][1]["haber"] = "1.00"
    r = client.put(f"{URL}/{asentado['id_asiento']}", headers=contador, json=datos)
    assert r.status_code == 422 and "diferencia" in r.json()["detail"]
    assert client.get(f"{URL}/{asentado['id_asiento']}", headers=contador).json()["estado"] == "ASENTADO"


def test_modificar_borrador_lo_reemplaza(client, db, contador, cuentas):
    borrador = client.post(URL, headers=contador, json=_asiento(cuentas, confirmar=False)).json()
    nuevo = client.put(
        f"{URL}/{borrador['id_asiento']}", headers=contador, json=_asiento(cuentas, confirmar=False, importe="50.00")
    ).json()
    assert nuevo["estado"] == "BORRADOR" and nuevo["id_asiento"] != borrador["id_asiento"]
    assert client.get(f"{URL}/{borrador['id_asiento']}", headers=contador).json()["estado"] == "ANULADO"
    assert db.query(AsientoContable).filter_by(tipo_origen="REVERSION").count() == 0


# ---------- Consulta (CUU-003) ----------


def test_filtros_del_libro_diario(client, contador, cuentas, asentado):
    client.post(URL, headers=contador, json={**_asiento(cuentas, debe="banco"), "fecha": "2026-10-15"})
    client.post(URL, headers=contador, json=_asiento(cuentas, confirmar=False))

    assert len(client.get(URL, headers=contador).json()) == 3
    assert len(client.get(URL, headers=contador, params={"desde": "2026-11-01"}).json()) == 2
    assert len(client.get(URL, headers=contador, params={"hasta": "2026-10-31"}).json()) == 1
    assert len(client.get(URL, headers=contador, params={"id_cuenta": cuentas["banco"]}).json()) == 1
    assert len(client.get(URL, headers=contador, params={"estado": "BORRADOR"}).json()) == 1
    assert len(client.get(URL, headers=contador, params={"tipo_origen": "VENTA"}).json()) == 0
    # 2.a / 2.b: sin resultados devuelve una lista vacía (la pantalla informa que no hay movimientos).
    assert client.get(URL, headers=contador, params={"desde": "2027-01-01"}).json() == []


def test_asiento_inexistente(client, contador):
    assert client.get(f"{URL}/999", headers=contador).status_code == 404


# ---------- Permisos ----------


@pytest.mark.parametrize("rol", [Rol.ADMINISTRADOR, Rol.CONSULTA])
def test_otros_perfiles_solo_consultan(client, crear_usuario, login, cuentas, asentado, rol):
    crear_usuario("lector@eugenia.com.ar", rol)
    headers = login("lector@eugenia.com.ar")
    assert client.get(URL, headers=headers).status_code == 200
    assert client.post(URL, headers=headers, json=_asiento(cuentas)).status_code == 403
    assert client.post(f"{URL}/{asentado['id_asiento']}/anular", headers=headers).status_code == 403


def test_administrativo_registra_asientos(client, crear_usuario, login, cuentas):
    crear_usuario("administrativo@eugenia.com.ar", Rol.ADMINISTRATIVO)
    headers = login("administrativo@eugenia.com.ar")
    assert client.post(URL, headers=headers, json=_asiento(cuentas)).status_code == 201
