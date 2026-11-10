"""CUU-001 Registrar venta (carga manual)."""

from decimal import Decimal

import pytest
from conftest import auditorias

from app.models import (
    AsientoContable,
    Cliente,
    CuentaPredeterminada,
    DetalleAsiento,
    EmpresaEmisora,
    PlanCuenta,
    Rol,
    Venta,
)

URL = "/api/ventas"


@pytest.fixture
def base(db):
    """Empresa emisora Responsable Inscripta, dos clientes (uno dado de baja), cuentas y predeterminadas."""
    db.add(EmpresaEmisora(id_emisor=1, razon_social="Distribuidora Andina S.A.", condicion_iva="Responsable Inscripto"))

    def cuenta(codigo, nombre, tipo, naturaleza):
        c = PlanCuenta(codigo=codigo, nombre=nombre, tipo_cuenta=tipo, imputable="1", activo="1", naturaleza=naturaleza)
        db.add(c)
        db.flush()
        return c.id_cuenta

    ids = {
        "caja": cuenta("1.1.1.01", "Caja", "ACTIVO", "DEUDORA"),
        "banco": cuenta("1.1.1.03", "Banco", "ACTIVO", "DEUDORA"),
        "deudores": cuenta("1.1.2.01", "Deudores por Ventas", "ACTIVO", "DEUDORA"),
        "iva": cuenta("2.1.3.01", "IVA Débito Fiscal", "PASIVO", "ACREEDORA"),
        "percepciones": cuenta("2.1.3.02", "Percepciones a Depositar", "PASIVO", "ACREEDORA"),
        "ventas": cuenta("4.1", "Ventas", "INGRESOS", "ACREEDORA"),
    }
    for clave, id_cuenta in {
        "CAJA": ids["caja"],
        "BANCO": ids["banco"],
        "DEUDORES_POR_VENTAS": ids["deudores"],
        "IVA_DEBITO_FISCAL": ids["iva"],
        "VENTAS": ids["ventas"],
    }.items():
        db.add(CuentaPredeterminada(clave=clave, id_cuenta=id_cuenta))
    cliente = Cliente(razon_social="Comercial Santa Fe S.R.L.", cuit="30-71234567-1", activo="1")
    baja = Cliente(razon_social="Cliente Inactivo S.A.", cuit="30-70000000-7", activo="0")
    db.add_all([cliente, baja])
    db.commit()
    return {**ids, "cliente": cliente.id_cliente, "cliente_baja": baja.id_cliente}


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


def _venta(base, confirmar=True, **extra):
    datos = {
        "id_cliente": base["cliente"],
        "tipo_comprobante": "Factura A",
        "punto_venta": 1,
        "numero_comprobante": 15,
        "fecha_emision": "2026-11-05",
        "condicion_venta": "Cuenta Corriente",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_total": "1210.00",
        "confirmar": confirmar,
    }
    datos.update(extra)
    return datos


def _lineas(db, id_venta):
    db.expire_all()
    asiento = db.query(AsientoContable).filter_by(id_venta=id_venta).one()
    detalle = db.query(DetalleAsiento).filter_by(id_asiento=asiento.id_asiento).all()
    return asiento, {(d.id_cuenta, d.debe, d.haber) for d in detalle}


# ---------- Camino básico (pasos 2-8) ----------


def test_venta_confirmada_genera_asiento_balanceado(client, db, contador, base):
    r = client.post(URL, headers=contador, json=_venta(base))
    assert r.status_code == 201, r.text
    venta = r.json()
    assert venta["estado"] == "CONTABILIZADA" and venta["numero"] == "0001-00000015"
    assert venta["fecha_contable"] == "2026-11-05" and venta["moneda"] == "ARS"
    assert venta["asiento"]["numero_asiento"] == 1 and venta["asiento"]["estado"] == "ASENTADO"

    asiento, lineas = _lineas(db, venta["id_venta"])
    assert asiento.tipo_origen == "VENTA" and asiento.referencia == "Factura A 0001-00000015"
    assert "Comercial Santa Fe" in asiento.concepto
    assert lineas == {
        (base["deudores"], Decimal("1210.00"), Decimal("0.00")),
        (base["ventas"], Decimal("0.00"), Decimal("1000.00")),
        (base["iva"], Decimal("0.00"), Decimal("210.00")),
    }
    assert len(auditorias(db, "CONTABILIZACION")) == 1


@pytest.mark.parametrize(("condicion", "cuenta"), [("Contado", "caja"), ("Transferencia", "banco")])
def test_cuenta_del_debe_segun_condicion_de_cobro(client, db, contador, base, condicion, cuenta):
    venta = client.post(URL, headers=contador, json=_venta(base, condicion_venta=condicion)).json()
    _, lineas = _lineas(db, venta["id_venta"])
    assert (base[cuenta], Decimal("1210.00"), Decimal("0.00")) in lineas


def test_fecha_contable_distinta_de_emision(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base, fecha_contable="2026-11-08")).json()
    asiento, _ = _lineas(db, venta["id_venta"])
    assert str(asiento.fecha) == "2026-11-08"


def test_fecha_contable_anterior_a_emision(client, contador, base):
    r = client.post(URL, headers=contador, json=_venta(base, fecha_contable="2026-11-01"))
    assert r.status_code == 422


def test_otros_impuestos_usan_su_cuenta_predeterminada(client, db, contador, base):
    db.add(CuentaPredeterminada(clave="OTROS_IMPUESTOS_VENTAS", id_cuenta=base["percepciones"]))
    db.commit()
    datos = _venta(base, importe_otros_impuestos="30.00", importe_total="1240.00")
    venta = client.post(URL, headers=contador, json=datos).json()
    _, lineas = _lineas(db, venta["id_venta"])
    assert (base["percepciones"], Decimal("0.00"), Decimal("30.00")) in lineas


def test_propuesta_no_guarda(client, db, contador, base):  # paso 6
    r = client.post(f"{URL}/propuesta", headers=contador, json=_venta(base))
    assert r.status_code == 200, r.text
    p = r.json()
    assert p["balanceado"] and p["cuentas_faltantes"] == [] and p["duplicado"] is None
    assert [linea["codigo"] for linea in p["lineas"]] == ["1.1.2.01", "4.1", "2.1.3.01"]
    assert db.query(Venta).count() == 0


# ---------- Pendiente (6.a) y contabilización posterior ----------


def test_venta_pendiente_no_genera_asiento(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base, confirmar=False)).json()
    assert venta["estado"] == "PENDIENTE" and venta["asiento"] is None
    assert db.query(AsientoContable).count() == 0


def test_contabilizar_pendiente(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base, confirmar=False)).json()
    r = client.post(f"{URL}/{venta['id_venta']}/contabilizar", headers=contador)
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == "CONTABILIZADA" and r.json()["asiento"]["numero_asiento"] == 1


def test_modificar_pendiente(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base, confirmar=False)).json()
    datos = _venta(base, confirmar=False, importe_neto_gravado="2000.00", importe_iva="420.00", importe_total="2420.00")
    r = client.put(f"{URL}/{venta['id_venta']}", headers=contador, json=datos)
    assert r.status_code == 200 and r.json()["importe_total"] == "2420.00"
    assert len(auditorias(db, "MODIFICACION")) == 1


def test_no_se_modifica_una_venta_contabilizada(client, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base)).json()
    r = client.put(f"{URL}/{venta['id_venta']}", headers=contador, json=_venta(base))
    assert r.status_code == 409


# ---------- 2.a Duplicado ----------


def test_comprobante_duplicado(client, db, contador, base):
    client.post(URL, headers=contador, json=_venta(base))
    r = client.post(URL, headers=contador, json=_venta(base))
    assert r.status_code == 409 and "ya fue registrado" in r.json()["detail"]
    assert db.query(Venta).count() == 1 and db.query(AsientoContable).count() == 1

    p = client.post(f"{URL}/propuesta", headers=contador, json=_venta(base)).json()
    assert p["duplicado"]["numero"] == "0001-00000015"


def test_mismo_numero_con_otro_tipo_no_es_duplicado(client, contador, base):
    client.post(URL, headers=contador, json=_venta(base))
    r = client.post(URL, headers=contador, json=_venta(base, tipo_comprobante="Factura B"))
    assert r.status_code == 201


def test_comprobante_de_venta_anulada_puede_registrarse(client, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base)).json()
    client.post(f"{URL}/{venta['id_venta']}/anular", headers=contador)
    assert client.post(URL, headers=contador, json=_venta(base)).status_code == 201


# ---------- 3 Cliente ----------


def test_cliente_dado_de_baja(client, contador, base):
    r = client.post(URL, headers=contador, json=_venta(base, id_cliente=base["cliente_baja"]))
    assert r.status_code == 422 and "dado de baja" in r.json()["detail"]


def test_cliente_inexistente(client, contador, base):
    assert client.post(URL, headers=contador, json=_venta(base, id_cliente=999)).status_code == 422


# ---------- 4.a / 4.b Cuentas ----------


def test_cuenta_no_determinada(client, db, contador, base):
    db.query(CuentaPredeterminada).filter_by(clave="DEUDORES_POR_VENTAS").delete()
    db.commit()
    p = client.post(f"{URL}/propuesta", headers=contador, json=_venta(base)).json()
    assert p["cuentas_faltantes"] == ["Deudores por ventas"] and p["lineas"][0]["id_cuenta"] is None

    r = client.post(URL, headers=contador, json=_venta(base))
    assert r.status_code == 422 and "Deudores por ventas" in r.json()["detail"]
    assert db.query(Venta).count() == 0

    # 4.a.2: el usuario selecciona la cuenta
    r = client.post(URL, headers=contador, json=_venta(base, cuentas={"cobro": base["deudores"]}))
    assert r.status_code == 201, r.text


def test_venta_pendiente_sin_cuenta_determinada(client, db, contador, base):  # 4.a.1: queda pendiente
    db.query(CuentaPredeterminada).filter_by(clave="VENTAS").delete()
    db.commit()
    r = client.post(URL, headers=contador, json=_venta(base, confirmar=False))
    assert r.status_code == 201 and r.json()["estado"] == "PENDIENTE"
    r = client.post(f"{URL}/{r.json()['id_venta']}/contabilizar", headers=contador, json={"ventas": base["ventas"]})
    assert r.status_code == 200 and r.json()["estado"] == "CONTABILIZADA"


# ---------- 5.a Importes ----------


def test_total_que_no_coincide_no_se_contabiliza(client, db, contador, base):
    datos = _venta(base, importe_total="1200.00")
    p = client.post(f"{URL}/propuesta", headers=contador, json=datos).json()
    assert not p["balanceado"] and Decimal(p["diferencia"]) == Decimal("-10.00")

    r = client.post(URL, headers=contador, json=datos)
    assert r.status_code == 422 and "diferencia 10.00" in r.json()["detail"]
    assert db.query(Venta).count() == 0

    # Se puede guardar pendiente de revisión, pero no contabilizar hasta corregirlo.
    venta = client.post(URL, headers=contador, json={**datos, "confirmar": False}).json()
    assert client.post(f"{URL}/{venta['id_venta']}/contabilizar", headers=contador).status_code == 422


def test_neto_cero(client, contador, base):
    datos = _venta(base, importe_neto_gravado="0", importe_iva="0", importe_total="0")
    assert client.post(URL, headers=contador, json=datos).status_code == 422


# ---------- Validaciones fiscales mínimas ----------


def test_factura_c_no_discrimina_iva(client, db, contador, base):
    db.get(EmpresaEmisora, 1).condicion_iva = "Monotributo"
    db.commit()
    r = client.post(URL, headers=contador, json=_venta(base, tipo_comprobante="Factura C"))
    assert r.status_code == 422 and "no discrimina IVA" in r.json()["detail"]
    datos = _venta(base, tipo_comprobante="Factura C", importe_iva="0", importe_total="1000.00")
    assert client.post(URL, headers=contador, json=datos).status_code == 201


def test_responsable_inscripto_no_emite_factura_c(client, contador, base):
    datos = _venta(base, tipo_comprobante="Factura C", importe_iva="0", importe_total="1000.00")
    r = client.post(URL, headers=contador, json=datos)
    assert r.status_code == 422 and "Factura A o Factura B" in r.json()["detail"]


def test_sin_empresa_emisora(client, db, contador, base):
    db.delete(db.get(EmpresaEmisora, 1))
    db.commit()
    assert client.post(URL, headers=contador, json=_venta(base)).status_code == 409


# ---------- Anulación ----------


def test_anular_venta_contabilizada_revierte_el_asiento(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base)).json()
    r = client.post(f"{URL}/{venta['id_venta']}/anular", headers=contador)
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == "ANULADA"
    assert r.json()["asiento"]["estado"] == "ANULADO" and r.json()["asiento"]["revertido_por"] == 2
    db.expire_all()
    contra = db.query(AsientoContable).filter_by(tipo_origen="REVERSION").one()
    saldo = {}
    for d in db.query(DetalleAsiento).all():
        saldo[d.id_cuenta] = saldo.get(d.id_cuenta, 0) + d.debe - d.haber
    assert contra.numero_asiento == 2 and all(v == 0 for v in saldo.values())
    assert db.query(Venta).count() == 1  # baja lógica: no se borra
    assert client.post(f"{URL}/{venta['id_venta']}/anular", headers=contador).status_code == 409


def test_anular_venta_pendiente(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base, confirmar=False)).json()
    r = client.post(f"{URL}/{venta['id_venta']}/anular", headers=contador)
    assert r.json()["estado"] == "ANULADA" and db.query(AsientoContable).count() == 0


def test_venta_con_cae_no_se_anula(client, db, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base)).json()
    db.get(Venta, venta["id_venta"]).cae = "74123456789012"
    db.commit()
    r = client.post(f"{URL}/{venta['id_venta']}/anular", headers=contador)
    assert r.status_code == 409 and "nota de crédito" in r.json()["detail"]


def test_asiento_de_venta_no_se_anula_desde_el_libro_diario(client, contador, base):
    venta = client.post(URL, headers=contador, json=_venta(base)).json()
    r = client.post(f"/api/asientos/{venta['asiento']['id_asiento']}/anular", headers=contador)
    assert r.status_code == 409


# ---------- Consulta y permisos ----------


def test_listar_con_filtros(client, contador, base):
    client.post(URL, headers=contador, json=_venta(base))
    client.post(URL, headers=contador, json=_venta(base, numero_comprobante=16, confirmar=False))
    assert len(client.get(URL, headers=contador).json()) == 2
    assert len(client.get(URL, headers=contador, params={"estado": "PENDIENTE"}).json()) == 1
    assert client.get(URL, headers=contador, params={"buscar": "0001-00000016"}).json()[0]["numero_comprobante"] == 16
    assert len(client.get(URL, headers=contador, params={"buscar": "santa fe"}).json()) == 2
    assert client.get(URL, headers=contador, params={"desde": "2026-11-06"}).json() == []


@pytest.mark.parametrize("rol", [Rol.CONSULTA, Rol.ADMINISTRADOR])
def test_roles_sin_permiso_solo_consultan(client, crear_usuario, login, base, rol):
    crear_usuario("otro@eugenia.com.ar", rol)
    headers = login("otro@eugenia.com.ar")
    assert client.post(URL, headers=headers, json=_venta(base)).status_code == 403
    assert client.get(URL, headers=headers).status_code == 200


def test_administrativo_registra(client, crear_usuario, login, base):
    crear_usuario("adm@eugenia.com.ar", Rol.ADMINISTRATIVO)
    assert client.post(URL, headers=login("adm@eugenia.com.ar"), json=_venta(base)).status_code == 201


def test_sin_sesion(client, base):
    assert client.get(URL).status_code == 401
