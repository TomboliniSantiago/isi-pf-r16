"""CUU-008 Gestionar Proveedores."""

import json
from datetime import date
from decimal import Decimal

import pytest
from conftest import auditorias

from app.arca.padron import DatosPadron, PadronSimulado, get_padron
from app.main import app
from app.models import AsientoContable, Compra, Proveedor, Rol

URL = "/api/proveedores"
NUEVO = {
    "cuit": "30-71045678-6",
    "razon_social": "Insumos Gráficos del Sur S.A.",
    "condicion_iva": "Responsable Inscripto",
    "domicilio": "Av. Peñaloza 7400",
    "localidad": "Santa Fe",
    "provincia": "Santa Fe",
}


@pytest.fixture(autouse=True)
def padron(db):
    simulado = PadronSimulado(
        [
            DatosPadron(
                NUEVO["cuit"], NUEVO["razon_social"], NUEVO["condicion_iva"], NUEVO["domicilio"], "Santa Fe", "Santa Fe"
            )
        ]
    )
    app.dependency_overrides[get_padron] = lambda: simulado
    return simulado


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


@pytest.fixture
def proveedor(client, contador):
    r = client.post(URL, headers=contador, json=NUEVO)
    assert r.status_code == 201, r.text
    return r.json()


def _compra(db, id_proveedor: int, estado_asiento: str | None) -> None:
    compra = Compra(
        id_emisor=1,
        id_proveedor=id_proveedor,
        tipo_comprobante="Factura A",
        punto_venta=3,
        numero_comprobante=1520,
        fecha_emision=date(2026, 11, 2),
        moneda="ARS",
        importe_total=Decimal("363000.00"),
    )
    db.add(compra)
    db.flush()
    if estado_asiento:
        db.add(
            AsientoContable(
                numero_asiento=1,
                fecha=date(2026, 11, 2),
                concepto="Compra",
                id_compra=compra.id_compra,
                estado=estado_asiento,
            )
        )
    db.commit()


# ---------- Alta (pasos 2-6) ----------


def test_consulta_padron_completa_los_datos(client, contador):  # paso 3
    cuerpo = client.get(f"{URL}/consulta-cuit", headers=contador, params={"cuit": "30710456786"}).json()
    assert cuerpo["cuit"] == NUEVO["cuit"] and cuerpo["en_padron"] is True
    assert cuerpo["datos"]["razon_social"] == NUEVO["razon_social"]
    assert cuerpo["proveedor_existente"] is None


def test_alta_asigna_codigo_y_audita(client, db, proveedor):  # paso 6
    assert proveedor["codigo"] == f"PRV-{proveedor['id_proveedor']:06d}"
    assert db.get(Proveedor, proveedor["id_proveedor"]).activo == "1"
    alta = auditorias(db, "ALTA")
    assert len(alta) == 1 and alta[0].tabla_afectada == "PROVEEDOR"


def test_cuit_duplicado(client, contador, proveedor):  # 4.a
    r = client.get(f"{URL}/consulta-cuit", headers=contador, params={"cuit": NUEVO["cuit"]})
    assert r.json()["proveedor_existente"]["codigo"] == proveedor["codigo"]
    r = client.post(URL, headers=contador, json={**NUEVO, "razon_social": "Otra"})
    assert r.status_code == 409 and proveedor["codigo"] in r.json()["detail"]


def test_mismo_cuit_puede_ser_cliente_y_proveedor(client, contador, proveedor):
    r = client.post("/api/clientes", headers=contador, json=NUEVO)
    assert r.status_code == 201


@pytest.mark.parametrize("cambio", [{"cuit": "30-71045678-0"}, {"razon_social": ""}, {"condicion_iva": "Otra"}])
def test_alta_rechaza_datos_invalidos(client, db, contador, cambio):
    assert client.post(URL, headers=contador, json={**NUEVO, **cambio}).status_code == 422
    assert db.query(Proveedor).count() == 0


# ---------- Modificación (2.a) ----------


def test_modificacion_audita_antes_y_despues(client, db, contador, proveedor):
    r = client.put(f"{URL}/{proveedor['id_proveedor']}", headers=contador, json={**NUEVO, "domicilio": "Ruta 168 Km 5"})
    assert r.status_code == 200
    registro = auditorias(db, "MODIFICACION")[0]
    assert json.loads(registro.datos_anteriores)["domicilio"] == NUEVO["domicilio"]
    assert json.loads(registro.datos_nuevos)["domicilio"] == "Ruta 168 Km 5"


def test_cambio_de_cuit_con_comprobantes(client, db, contador, proveedor):
    _compra(db, proveedor["id_proveedor"], estado_asiento="ASENTADO")
    r = client.put(f"{URL}/{proveedor['id_proveedor']}", headers=contador, json={**NUEVO, "cuit": "20-25789456-9"})
    assert r.status_code == 409 and "comprobantes asociados" in r.json()["detail"]


# ---------- Consulta (2.c) ----------


def test_detalle_e_historial_de_comprobantes(client, db, contador, proveedor):
    _compra(db, proveedor["id_proveedor"], estado_asiento="BORRADOR")
    detalle = client.get(f"{URL}/{proveedor['id_proveedor']}", headers=contador).json()
    assert detalle["cantidad_comprobantes"] == 1 and detalle["comprobantes_pendientes"] == 1
    compras = client.get(f"{URL}/{proveedor['id_proveedor']}/comprobantes", headers=contador).json()
    assert compras[0]["numero"] == "0003-00001520" and compras[0]["pendiente"] is True


def test_busqueda_por_cuit_o_razon_social(client, contador, proveedor):
    assert len(client.get(URL, headers=contador, params={"buscar": "71045678"}).json()) == 1
    assert len(client.get(URL, headers=contador, params={"buscar": "gráficos"}).json()) == 1
    assert client.get(URL, headers=contador, params={"activo": False}).json() == []


# ---------- Baja (2.b) y reactivación ----------


@pytest.mark.parametrize("estado_asiento", [None, "BORRADOR"])
def test_baja_bloqueada_por_compra_sin_asentar(client, db, contador, proveedor, estado_asiento):
    _compra(db, proveedor["id_proveedor"], estado_asiento=estado_asiento)
    r = client.post(f"{URL}/{proveedor['id_proveedor']}/baja", headers=contador)
    assert r.status_code == 409 and "sin asiento asentado" in r.json()["detail"]


def test_baja_y_reactivacion(client, db, contador, proveedor):
    _compra(db, proveedor["id_proveedor"], estado_asiento="ASENTADO")
    url = f"{URL}/{proveedor['id_proveedor']}"
    assert client.get(f"{url}/verificar-baja", headers=contador).json()["valido"] is True
    assert client.post(f"{url}/baja", headers=contador).json()["activo"] is False
    assert db.get(Proveedor, proveedor["id_proveedor"]).activo == "0"
    assert client.post(f"{url}/reactivar", headers=contador).json()["activo"] is True
    assert len(auditorias(db, "BAJA")) == 1 and len(auditorias(db, "REACTIVACION")) == 1


# ---------- Permisos ----------


@pytest.mark.parametrize("rol", [Rol.ADMINISTRADOR, Rol.CONSULTA])
def test_otros_perfiles_solo_consultan(client, crear_usuario, login, proveedor, rol):
    crear_usuario("lector@eugenia.com.ar", rol)
    headers = login("lector@eugenia.com.ar")
    assert client.get(URL, headers=headers).status_code == 200
    assert client.post(URL, headers=headers, json={**NUEVO, "cuit": "20-25789456-9"}).status_code == 403
    assert client.post(f"{URL}/{proveedor['id_proveedor']}/baja", headers=headers).status_code == 403


def test_administrativo_puede_editar(client, crear_usuario, login):
    crear_usuario("administrativo@eugenia.com.ar", Rol.ADMINISTRATIVO)
    assert client.post(URL, headers=login("administrativo@eugenia.com.ar"), json=NUEVO).status_code == 201
