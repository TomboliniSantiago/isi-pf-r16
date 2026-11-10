"""CUU-005 Gestionar Plan de Cuentas."""

import json
from datetime import date
from decimal import Decimal

import pytest
from conftest import auditorias

from app.models import AsientoContable, DetalleAsiento, PlanCuenta, Rol

URL = "/api/plan-cuentas"


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


@pytest.fixture
def alta(client, contador):
    """Da de alta una cuenta y devuelve su id."""

    def _alta(codigo, nombre, tipo="ACTIVO", padre=None, imputable=False, naturaleza=None, esperado=201):
        datos = {
            "codigo": codigo,
            "nombre": nombre,
            "tipo_cuenta": tipo,
            "imputable": imputable,
            "naturaleza": naturaleza,
            "id_cuenta_padre": padre,
        }
        r = client.post(URL, headers=contador, json=datos)
        assert r.status_code == esperado, r.text
        return r.json().get("id_cuenta") if esperado == 201 else r.json()["detail"]

    return _alta


@pytest.fixture
def estructura(alta):
    """1 ACTIVO > 1.1 Activo Corriente > 1.1.1 Caja y Bancos > 1.1.1.01 Caja (imputable)."""
    activo = alta("1", "ACTIVO")
    corriente = alta("1.1", "Activo Corriente", padre=activo)
    caja_bancos = alta("1.1.1", "Caja y Bancos", padre=corriente)
    caja = alta("1.1.1.01", "Caja", padre=caja_bancos, imputable=True, naturaleza="DEUDORA")
    return {"activo": activo, "corriente": corriente, "caja_bancos": caja_bancos, "caja": caja}


def _datos(cuenta: dict, **cambios) -> dict:
    campos = ("codigo", "nombre", "tipo_cuenta", "naturaleza", "imputable", "id_cuenta_padre")
    return {**{k: cuenta[k] for k in campos}, **cambios}


def _movimiento(db, id_cuenta: int) -> None:
    asiento = AsientoContable(numero_asiento=1, fecha=date(2026, 11, 5), concepto="Apertura", estado="CONFIRMADO")
    db.add(asiento)
    db.flush()
    db.add(DetalleAsiento(id_asiento=asiento.id_asiento, id_cuenta=id_cuenta, debe=Decimal("1000"), haber=Decimal("0")))
    db.commit()


# ---------- Alta (pasos 2-6) ----------


def test_alta_y_listado_jerarquico(client, db, contador, estructura):
    cuentas = client.get(URL, headers=contador).json()
    assert [c["codigo"] for c in cuentas] == ["1", "1.1", "1.1.1", "1.1.1.01"]
    caja = cuentas[-1]
    assert caja["nivel"] == 4
    assert caja["codigo_padre"] == "1.1.1"
    assert caja["imputable"] is True and caja["activa"] is True
    assert caja["naturaleza"] == "DEUDORA"
    alta = auditorias(db, "ALTA")
    assert len(alta) == 4 and alta[0].tabla_afectada == "PLAN_CUENTA"


def test_listado_ordena_codigos_numericamente(client, contador, alta):
    activo = alta("1", "ACTIVO")
    for codigo in ("1.10", "1.2", "1.1"):
        alta(codigo, f"Cuenta {codigo}", padre=activo)
    assert [c["codigo"] for c in client.get(URL, headers=contador).json()] == ["1", "1.1", "1.2", "1.10"]


def test_codigo_duplicado(alta, estructura, client, contador):  # 4.a
    detalle = alta(
        "1.1.1.01", "Otra caja", padre=estructura["caja_bancos"], imputable=True, naturaleza="DEUDORA", esperado=409
    )
    assert "ya está registrado" in detalle


@pytest.mark.parametrize(
    ("codigo", "mensaje"),
    [("1.a", "números separados por puntos"), ("1..2", "números separados por puntos"), ("1.1", "un solo nivel")],
)
def test_formato_de_codigo_sin_padre(alta, codigo, mensaje):
    assert mensaje in alta(codigo, "Rubro", esperado=422)


@pytest.mark.parametrize(
    ("codigo", "tipo", "imputable", "naturaleza", "mensaje"),
    [
        ("2.1", "ACTIVO", False, None, "comenzar con el de la cuenta padre"),
        ("1.1.9", "PASIVO", False, None, "coincidir con el de la cuenta padre"),
        ("1.1.9", "ACTIVO", True, None, "naturaleza"),
    ],
)
def test_jerarquia_inconsistente(alta, estructura, codigo, tipo, imputable, naturaleza, mensaje):  # 4.b
    detalle = alta(
        codigo, "X", tipo=tipo, padre=estructura["corriente"], imputable=imputable, naturaleza=naturaleza, esperado=422
    )
    assert mensaje in detalle


def test_padre_imputable_o_inexistente(alta, estructura):
    assert "es imputable" in alta("1.1.1.01.1", "X", padre=estructura["caja"], esperado=422)
    assert "no existe" in alta("1.9", "X", padre=999, esperado=422)


def test_padre_dado_de_baja(client, contador, alta, estructura):
    rubro = alta("1.2", "Activo No Corriente", padre=estructura["activo"])
    assert client.post(f"{URL}/{rubro}/baja", headers=contador).status_code == 200
    assert "dada de baja" in alta("1.2.1", "Bienes de Uso", padre=rubro, esperado=422)


def test_validar_no_guarda(client, db, contador, estructura):  # paso 5
    datos = {
        "codigo": "1.1.2",
        "nombre": "Créditos",
        "tipo_cuenta": "ACTIVO",
        "imputable": False,
        "id_cuenta_padre": estructura["corriente"],
    }
    r = client.post(f"{URL}/validar", headers=contador, json=datos)
    assert r.status_code == 200 and r.json()["valido"] is True
    assert db.query(PlanCuenta).count() == 4
    r = client.post(f"{URL}/validar", headers=contador, json={**datos, "codigo": "1.1.1"})
    assert r.status_code == 409


# ---------- Modificación (2.a) ----------


def test_modificacion_audita_antes_y_despues(client, db, contador, estructura):
    caja = client.get(f"{URL}/{estructura['caja']}", headers=contador).json()
    r = client.put(f"{URL}/{caja['id_cuenta']}", headers=contador, json=_datos(caja, nombre="Caja chica"))
    assert r.status_code == 200 and r.json()["nombre"] == "Caja chica"
    registro = auditorias(db, "MODIFICACION")[0]
    assert json.loads(registro.datos_anteriores)["nombre"] == "Caja"
    assert json.loads(registro.datos_nuevos)["nombre"] == "Caja chica"
    assert registro.usuario == "contador@eugenia.com.ar"


def test_modificacion_con_hijas(client, contador, estructura):
    rubro = client.get(f"{URL}/{estructura['caja_bancos']}", headers=contador).json()
    url = f"{URL}/{rubro['id_cuenta']}"
    assert client.put(url, headers=contador, json=_datos(rubro, codigo="1.1.5")).status_code == 409
    assert (
        client.put(url, headers=contador, json=_datos(rubro, imputable=True, naturaleza="DEUDORA")).status_code == 409
    )
    assert client.put(url, headers=contador, json=_datos(rubro, nombre="Disponibilidades")).status_code == 200


def test_modificacion_con_movimientos(client, db, contador, estructura):
    _movimiento(db, estructura["caja"])
    caja = client.get(f"{URL}/{estructura['caja']}", headers=contador).json()
    url = f"{URL}/{caja['id_cuenta']}"
    r = client.put(url, headers=contador, json=_datos(caja, imputable=False, naturaleza=None))
    assert r.status_code == 409 and "movimientos" in r.json()["detail"]
    assert client.put(url, headers=contador, json=_datos(caja, nombre="Caja central")).status_code == 200


# ---------- Baja lógica (2.b) y reactivación ----------


def test_baja_con_hijas_activas(client, contador, estructura):
    r = client.post(f"{URL}/{estructura['caja_bancos']}/baja", headers=contador)
    assert r.status_code == 409 and "dependientes activas" in r.json()["detail"]


def test_baja_con_movimientos(client, db, contador, estructura):
    _movimiento(db, estructura["caja"])
    assert client.get(f"{URL}/{estructura['caja']}/verificar-baja", headers=contador).status_code == 409
    r = client.post(f"{URL}/{estructura['caja']}/baja", headers=contador)
    assert r.status_code == 409 and "movimientos" in r.json()["detail"]


def test_baja_logica_conserva_la_cuenta(client, db, contador, estructura):
    assert client.get(f"{URL}/{estructura['caja']}/verificar-baja", headers=contador).json()["valido"] is True
    r = client.post(f"{URL}/{estructura['caja']}/baja", headers=contador)
    assert r.status_code == 200 and r.json()["activa"] is False
    assert db.get(PlanCuenta, estructura["caja"]) is not None
    assert len(auditorias(db, "BAJA")) == 1
    # El código sigue reservado aunque la cuenta esté dada de baja.
    datos = {
        "codigo": "1.1.1.01",
        "nombre": "Caja",
        "tipo_cuenta": "ACTIVO",
        "imputable": True,
        "naturaleza": "DEUDORA",
        "id_cuenta_padre": estructura["caja_bancos"],
    }
    r = client.post(URL, headers=contador, json=datos)
    assert r.status_code == 409 and "dada de baja" in r.json()["detail"]


def test_reactivar_exige_padre_activo(client, contador, estructura):
    for cuenta in ("caja", "caja_bancos"):
        assert client.post(f"{URL}/{estructura[cuenta]}/baja", headers=contador).status_code == 200
    r = client.post(f"{URL}/{estructura['caja']}/reactivar", headers=contador)
    assert r.status_code == 409 and "padre" in r.json()["detail"]
    assert client.post(f"{URL}/{estructura['caja_bancos']}/reactivar", headers=contador).status_code == 200
    assert client.post(f"{URL}/{estructura['caja']}/reactivar", headers=contador).json()["activa"] is True


# ---------- Consulta (2.c) ----------


def test_detalle_con_ruta_y_movimientos(client, db, contador, estructura):
    _movimiento(db, estructura["caja"])
    detalle = client.get(f"{URL}/{estructura['caja']}", headers=contador).json()
    assert [c["codigo"] for c in detalle["ruta"]] == ["1", "1.1", "1.1.1"]
    assert detalle["cantidad_movimientos"] == 1
    assert detalle["cantidad_hijas"] == 0
    movs = client.get(f"{URL}/{estructura['caja']}/movimientos", headers=contador).json()
    assert len(movs) == 1 and movs[0]["concepto"] == "Apertura" and Decimal(movs[0]["debe"]) == 1000


def test_filtros(client, contador, estructura):
    imputables = client.get(URL, headers=contador, params={"imputable": True}).json()
    assert [c["codigo"] for c in imputables] == ["1.1.1.01"]
    assert [c["codigo"] for c in client.get(URL, headers=contador, params={"buscar": "bancos"}).json()] == ["1.1.1"]
    assert client.get(URL, headers=contador, params={"tipo": "PASIVO"}).json() == []


def test_consulta_de_cuenta_inexistente(client, contador):
    assert client.get(f"{URL}/999", headers=contador).status_code == 404


# ---------- Permisos ----------


@pytest.mark.parametrize("rol", [Rol.ADMINISTRATIVO, Rol.CONSULTA])
def test_perfiles_de_solo_lectura(client, crear_usuario, login, estructura, rol):
    crear_usuario("lector@eugenia.com.ar", rol)
    headers = login("lector@eugenia.com.ar")
    assert client.get(URL, headers=headers).status_code == 200
    datos = {"codigo": "2", "nombre": "PASIVO", "tipo_cuenta": "PASIVO", "imputable": False}
    assert client.post(URL, headers=headers, json=datos).status_code == 403
    assert client.post(f"{URL}/{estructura['caja']}/baja", headers=headers).status_code == 403


def test_administrador_puede_editar(client, admin):
    _, headers = admin
    datos = {"codigo": "2", "nombre": "PASIVO", "tipo_cuenta": "PASIVO", "imputable": False}
    assert client.post(URL, headers=headers, json=datos).status_code == 201


def test_sin_sesion(client):
    assert client.get(URL).status_code == 401


# ---------- Cuentas predeterminadas ----------


def test_predeterminadas(client, db, contador, estructura):
    claves = client.get(f"{URL}/predeterminadas", headers=contador).json()
    assert len(claves) == 11 and all(c["cuenta"] is None for c in claves)

    r = client.put(f"{URL}/predeterminadas/VENTAS", headers=contador, json={"id_cuenta": estructura["caja_bancos"]})
    assert r.status_code == 422  # no imputable

    r = client.put(
        f"{URL}/predeterminadas/DEUDORES_POR_VENTAS", headers=contador, json={"id_cuenta": estructura["caja"]}
    )
    assert r.status_code == 200 and r.json()["cuenta"]["codigo"] == "1.1.1.01"
    assert len(auditorias(db, "PREDETERMINADA")) == 1
    assert client.get(f"{URL}/{estructura['caja']}", headers=contador).json()["predeterminada_para"] == [
        "DEUDORES_POR_VENTAS"
    ]

    r = client.post(f"{URL}/{estructura['caja']}/baja", headers=contador)
    assert r.status_code == 409 and "predeterminada" in r.json()["detail"]

    r = client.put(f"{URL}/predeterminadas/DEUDORES_POR_VENTAS", headers=contador, json={"id_cuenta": None})
    assert r.status_code == 200 and r.json()["cuenta"] is None
    assert client.post(f"{URL}/{estructura['caja']}/baja", headers=contador).status_code == 200


def test_predeterminadas_solo_editan_contador_y_admin(client, crear_usuario, login, estructura):
    crear_usuario("consulta@eugenia.com.ar", Rol.CONSULTA)
    headers = login("consulta@eugenia.com.ar")
    assert client.get(f"{URL}/predeterminadas", headers=headers).status_code == 200
    r = client.put(f"{URL}/predeterminadas/VENTAS", headers=headers, json={"id_cuenta": estructura["caja"]})
    assert r.status_code == 403


# ---------- Datos heredados y convenciones de la base ----------


def test_marcas_se_guardan_con_la_convencion_de_la_base(db, estructura):
    caja = db.get(PlanCuenta, estructura["caja"])
    assert (caja.imputable, caja.activo) == ("1", "1")
    assert db.get(PlanCuenta, estructura["caja_bancos"]).imputable == "0"


def test_cuenta_heredada_imputable_con_hijas(client, db, contador, estructura):
    """Como 1.1.1 en la base: imputable, con subcuentas y movimientos. Se puede editar su nombre,
    pero no agregarle más subcuentas."""
    rubro = db.get(PlanCuenta, estructura["caja_bancos"])
    rubro.imputable = "1"
    db.commit()
    _movimiento(db, rubro.id_cuenta)

    actual = client.get(f"{URL}/{rubro.id_cuenta}", headers=contador).json()
    datos = _datos(actual, nombre="Caja y Bancos (heredada)", naturaleza="DEUDORA")
    assert client.put(f"{URL}/{rubro.id_cuenta}", headers=contador, json=datos).status_code == 200

    nueva = {
        "codigo": "1.1.1.09",
        "nombre": "Otra",
        "tipo_cuenta": "ACTIVO",
        "imputable": False,
        "id_cuenta_padre": rubro.id_cuenta,
    }
    r = client.post(URL, headers=contador, json=nueva)
    assert r.status_code == 422 and "es imputable" in r.json()["detail"]


def test_cuenta_heredada_con_codigo_fuera_de_su_rubro(client, db, contador, estructura):
    """Como 2.1.2.02 IVA Crédito Fiscal bajo 1.1.2: se puede renombrar, y al corregir el código se valida."""
    heredada = PlanCuenta(
        codigo="2.1.2.02",
        nombre="IVA Crédito Fiscal",
        tipo_cuenta="ACTIVO",
        id_cuenta_padre=estructura["corriente"],
        imputable="1",
        activo="1",
    )
    db.add(heredada)
    db.commit()
    actual = client.get(f"{URL}/{heredada.id_cuenta}", headers=contador).json()
    url = f"{URL}/{heredada.id_cuenta}"

    assert (
        client.put(url, headers=contador, json=_datos(actual, nombre="IVA CF", naturaleza="DEUDORA")).status_code == 200
    )
    r = client.put(url, headers=contador, json=_datos(actual, codigo="2.1.2.03", naturaleza="DEUDORA"))
    assert r.status_code == 422 and "comenzar con el de la cuenta padre" in r.json()["detail"]
    assert (
        client.put(url, headers=contador, json=_datos(actual, codigo="1.1.9", naturaleza="DEUDORA")).status_code == 200
    )


def test_tipos_en_plural_como_en_la_base(alta):
    alta("4", "RESULTADOS POSITIVOS", tipo="INGRESOS")
    alta("5", "RESULTADOS NEGATIVOS", tipo="GASTOS")
    assert "tipo_cuenta" in alta("6", "Otro", tipo="INGRESO", esperado=422)


# ---------- Coherencia de las cuentas predeterminadas ----------


def _asignar(client, headers, clave, id_cuenta):
    return client.put(f"{URL}/predeterminadas/{clave}", headers=headers, json={"id_cuenta": id_cuenta})


def test_predeterminada_rechaza_tipo_incoherente(client, contador, estructura):
    r = _asignar(client, contador, "VENTAS", estructura["caja"])  # Caja es Activo
    assert r.status_code == 422
    assert r.json()["detail"] == "La cuenta para «Ventas» debe ser de tipo Ingresos, naturaleza acreedora."


def test_predeterminada_rechaza_naturaleza_incoherente(client, contador, alta, estructura):
    prevision = alta("1.1.1.09", "Previsión", padre=estructura["caja_bancos"], imputable=True, naturaleza="ACREEDORA")
    r = _asignar(client, contador, "DEUDORES_POR_VENTAS", prevision)  # Activo, pero regularizadora (acreedora)
    assert r.status_code == 422 and "naturaleza deudora" in r.json()["detail"]


def test_compras_admite_activo_o_gastos(client, contador, alta, estructura):
    gastos = alta("5", "RESULTADOS NEGATIVOS", tipo="GASTOS")
    compras = alta("5.1", "Compras", tipo="GASTOS", padre=gastos, imputable=True, naturaleza="DEUDORA")
    assert _asignar(client, contador, "COMPRAS", compras).status_code == 200
    assert _asignar(client, contador, "COMPRAS", estructura["caja"]).status_code == 200


def test_predeterminada_acepta_naturaleza_vacia_heredada(client, db, contador, estructura):
    caja = db.get(PlanCuenta, estructura["caja"])
    caja.naturaleza = None  # cuenta cargada antes de la migración 003
    db.commit()
    assert _asignar(client, contador, "IVA_CREDITO_FISCAL", caja.id_cuenta).status_code == 200


def test_cuenta_predeterminada_no_puede_quedar_incoherente(client, contador, estructura):
    assert _asignar(client, contador, "DEUDORES_POR_VENTAS", estructura["caja"]).status_code == 200
    caja = client.get(f"{URL}/{estructura['caja']}", headers=contador).json()
    url = f"{URL}/{caja['id_cuenta']}"

    r = client.put(url, headers=contador, json=_datos(caja, naturaleza="ACREEDORA"))
    assert r.status_code == 409 and "«Deudores por ventas»" in r.json()["detail"]
    r = client.put(url, headers=contador, json=_datos(caja, imputable=False, naturaleza=None))
    assert r.status_code == 409 and "debe seguir siendo imputable" in r.json()["detail"]
    assert client.put(url, headers=contador, json=_datos(caja, nombre="Caja central")).status_code == 200


def test_predeterminadas_informan_la_regla(client, contador):
    reglas = {p["clave"]: p for p in client.get(f"{URL}/predeterminadas", headers=contador).json()}
    assert reglas["COMPRAS"]["tipos_admitidos"] == ["ACTIVO", "GASTOS"]
    assert reglas["COMPRAS"]["requisito"] == "Activo o Gastos, naturaleza deudora"
    assert reglas["RESULTADO_EJERCICIO"]["naturaleza"] is None
    assert reglas["RESULTADO_EJERCICIO"]["requisito"] == "Patrimonio neto"
