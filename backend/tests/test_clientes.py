"""CUU-007 Gestionar Clientes."""

import json
from datetime import date
from decimal import Decimal

import pytest
from conftest import auditorias

from app.arca.padron import DatosPadron, PadronSimulado, get_padron
from app.main import app
from app.models import AsientoContable, Cliente, Rol, Venta

URL = "/api/clientes"
NUEVO = {
    "cuit": "30-71589631-8",
    "razon_social": "Electrónica del Centro S.A.",
    "condicion_iva": "Responsable Inscripto",
    "domicilio": "Av. Aristóbulo del Valle 5600",
    "localidad": "Santa Fe",
    "provincia": "Santa Fe",
}


@pytest.fixture(autouse=True)
def padron(db):
    """Padrón simulado con un contribuyente conocido (las pruebas no dependen de la lista de desarrollo)."""
    simulado = PadronSimulado(
        [
            DatosPadron(
                "30-71589631-8",
                "Electrónica del Centro S.A.",
                "Responsable Inscripto",
                "Av. Aristóbulo del Valle 5600",
                "Santa Fe",
                "Santa Fe",
            )
        ]
    )
    app.dependency_overrides[get_padron] = lambda: simulado
    return simulado


@pytest.fixture
def administrativo(crear_usuario, login):
    crear_usuario("administrativo@eugenia.com.ar", Rol.ADMINISTRATIVO)
    return login("administrativo@eugenia.com.ar")


@pytest.fixture
def cliente(client, administrativo):
    r = client.post(URL, headers=administrativo, json=NUEVO)
    assert r.status_code == 201, r.text
    return r.json()


def _venta(db, id_cliente: int, cae: str | None, estado_asiento: str | None) -> None:
    venta = Venta(
        id_emisor=1,
        id_cliente=id_cliente,
        tipo_comprobante="Factura A",
        punto_venta=1,
        numero_comprobante=7,
        fecha_emision=date(2026, 11, 2),
        moneda="ARS",
        importe_total=Decimal("121000.00"),
        cae=cae,
    )
    db.add(venta)
    db.flush()
    if estado_asiento:
        db.add(
            AsientoContable(
                numero_asiento=1,
                fecha=date(2026, 11, 2),
                concepto="Venta",
                id_venta=venta.id_venta,
                estado=estado_asiento,
            )
        )
    db.commit()


# ---------- Alta (pasos 2-6) ----------


def test_consulta_padron_completa_los_datos(client, administrativo):  # paso 3
    r = client.get(f"{URL}/consulta-cuit", headers=administrativo, params={"cuit": "30715896318"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["cuit"] == "30-71589631-8"  # normalizado
    assert cuerpo["en_padron"] is True
    assert cuerpo["datos"]["razon_social"] == "Electrónica del Centro S.A."
    assert cuerpo["cliente_existente"] is None


def test_cuit_que_no_figura_en_el_padron(client, administrativo):
    cuerpo = client.get(f"{URL}/consulta-cuit", headers=administrativo, params={"cuit": "20-31456789-8"}).json()
    assert cuerpo["en_padron"] is False and cuerpo["datos"] is None


def test_consulta_con_cuit_invalido(client, administrativo):
    r = client.get(f"{URL}/consulta-cuit", headers=administrativo, params={"cuit": "30-71589631-0"})
    assert r.status_code == 422 and "no es válido" in r.json()["detail"]


def test_alta_asigna_codigo_y_audita(client, db, cliente):  # paso 6
    assert cliente["codigo"] == f"CLI-{cliente['id_cliente']:06d}"
    assert cliente["activo"] is True
    assert db.get(Cliente, cliente["id_cliente"]).activo == "1"  # convención de la base
    alta = auditorias(db, "ALTA")
    assert len(alta) == 1 and alta[0].tabla_afectada == "CLIENTE"
    assert json.loads(alta[0].datos_nuevos)["cuit"] == "30-71589631-8"


def test_alta_normaliza_el_cuit(client, administrativo):
    r = client.post(URL, headers=administrativo, json={**NUEVO, "cuit": "30715896318"})
    assert r.status_code == 201 and r.json()["cuit"] == "30-71589631-8"


def test_cuit_duplicado(client, administrativo, cliente):  # 4.a
    r = client.get(f"{URL}/consulta-cuit", headers=administrativo, params={"cuit": NUEVO["cuit"]})
    assert r.json()["cliente_existente"]["codigo"] == cliente["codigo"]

    r = client.post(URL, headers=administrativo, json={**NUEVO, "razon_social": "Otra"})
    assert r.status_code == 409
    assert cliente["codigo"] in r.json()["detail"]


def test_cuit_duplicado_de_cliente_dado_de_baja(client, administrativo, cliente):
    client.post(f"{URL}/{cliente['id_cliente']}/baja", headers=administrativo)
    r = client.post(URL, headers=administrativo, json=NUEVO)
    assert r.status_code == 409 and "dado de baja" in r.json()["detail"]


@pytest.mark.parametrize(
    "cambio", [{"condicion_iva": "Inscripto"}, {"razon_social": ""}, {"domicilio": ""}, {"cuit": "123"}]
)
def test_alta_rechaza_datos_invalidos(client, db, administrativo, cambio):
    r = client.post(URL, headers=administrativo, json={**NUEVO, **cambio})
    assert r.status_code == 422
    assert db.query(Cliente).count() == 0


# ---------- Modificación (2.a) ----------


def test_modificacion_audita_antes_y_despues(client, db, administrativo, cliente):
    r = client.put(
        f"{URL}/{cliente['id_cliente']}", headers=administrativo, json={**NUEVO, "domicilio": "Ruta 11 Km 2"}
    )
    assert r.status_code == 200 and r.json()["domicilio"] == "Ruta 11 Km 2"
    registro = auditorias(db, "MODIFICACION")[0]
    assert json.loads(registro.datos_anteriores)["domicilio"] == NUEVO["domicilio"]
    assert json.loads(registro.datos_nuevos)["domicilio"] == "Ruta 11 Km 2"


def test_cambio_de_cuit(client, db, administrativo, cliente):
    url = f"{URL}/{cliente['id_cliente']}"
    assert client.put(url, headers=administrativo, json={**NUEVO, "cuit": "20-31456789-8"}).status_code == 200
    _venta(db, cliente["id_cliente"], cae="76123456789012", estado_asiento="ASENTADO")
    r = client.put(url, headers=administrativo, json={**NUEVO, "cuit": "30-71589631-8"})
    assert r.status_code == 409 and "comprobantes asociados" in r.json()["detail"]


# ---------- Consulta (2.b) ----------


def test_detalle_e_historial_de_comprobantes(client, db, administrativo, cliente):
    _venta(db, cliente["id_cliente"], cae=None, estado_asiento="ASENTADO")
    detalle = client.get(f"{URL}/{cliente['id_cliente']}", headers=administrativo).json()
    assert detalle["cantidad_comprobantes"] == 1 and detalle["comprobantes_pendientes"] == 1

    comprobantes = client.get(f"{URL}/{cliente['id_cliente']}/comprobantes", headers=administrativo).json()
    assert comprobantes[0]["numero"] == "0001-00000007"
    assert comprobantes[0]["asentado"] is True and comprobantes[0]["pendiente"] is True


def test_listado_y_filtros(client, db, administrativo, cliente):
    db.add(
        Cliente(
            cuit="27-40123456-5",
            razon_social="Valeria Sosa",
            condicion_iva="Consumidor Final",
            domicilio="Lavalle 3150",
            activo="0",
        )
    )
    db.commit()
    assert len(client.get(URL, headers=administrativo).json()) == 2
    assert [c["razon_social"] for c in client.get(URL, headers=administrativo, params={"activo": True}).json()] == [
        NUEVO["razon_social"]
    ]
    assert len(client.get(URL, headers=administrativo, params={"condicion_iva": "Consumidor Final"}).json()) == 1
    # Búsqueda por razón social y por CUIT con o sin guiones.
    assert len(client.get(URL, headers=administrativo, params={"buscar": "electrónica"}).json()) == 1
    assert len(client.get(URL, headers=administrativo, params={"buscar": "4012345"}).json()) == 1
    assert len(client.get(URL, headers=administrativo, params={"buscar": "30-7158"}).json()) == 1


def test_cliente_inexistente(client, administrativo):
    assert client.get(f"{URL}/999", headers=administrativo).status_code == 404


# ---------- Baja (2.c) y reactivación ----------


@pytest.mark.parametrize(
    ("cae", "estado_asiento"), [(None, "ASENTADO"), ("76123456789012", "BORRADOR"), ("76123456789012", None)]
)
def test_baja_bloqueada_por_comprobante_pendiente(client, db, administrativo, cliente, cae, estado_asiento):
    _venta(db, cliente["id_cliente"], cae=cae, estado_asiento=estado_asiento)
    assert client.get(f"{URL}/{cliente['id_cliente']}/verificar-baja", headers=administrativo).status_code == 409
    r = client.post(f"{URL}/{cliente['id_cliente']}/baja", headers=administrativo)
    assert r.status_code == 409 and "pendiente" in r.json()["detail"]


def test_baja_con_comprobantes_procesados(client, db, administrativo, cliente):
    _venta(db, cliente["id_cliente"], cae="76123456789012", estado_asiento="ASENTADO")
    assert client.get(f"{URL}/{cliente['id_cliente']}/verificar-baja", headers=administrativo).json()["valido"] is True
    r = client.post(f"{URL}/{cliente['id_cliente']}/baja", headers=administrativo)
    assert r.status_code == 200 and r.json()["activo"] is False
    assert db.get(Cliente, cliente["id_cliente"]).activo == "0"
    assert len(auditorias(db, "BAJA")) == 1


def test_reactivar(client, db, administrativo, cliente):
    url = f"{URL}/{cliente['id_cliente']}"
    client.post(f"{url}/baja", headers=administrativo)
    assert client.post(f"{url}/reactivar", headers=administrativo).json()["activo"] is True
    assert client.post(f"{url}/reactivar", headers=administrativo).status_code == 409
    assert len(auditorias(db, "REACTIVACION")) == 1


# ---------- Permisos ----------


@pytest.mark.parametrize("rol", [Rol.CONTADOR, Rol.ADMINISTRATIVO])
def test_actores_del_caso_de_uso_pueden_editar(client, crear_usuario, login, rol):
    crear_usuario("actor@eugenia.com.ar", rol)
    assert client.post(URL, headers=login("actor@eugenia.com.ar"), json=NUEVO).status_code == 201


@pytest.mark.parametrize("rol", [Rol.ADMINISTRADOR, Rol.CONSULTA])
def test_otros_perfiles_solo_consultan(client, crear_usuario, login, cliente, rol):
    crear_usuario("lector@eugenia.com.ar", rol)
    headers = login("lector@eugenia.com.ar")
    assert client.get(URL, headers=headers).status_code == 200
    assert client.get(f"{URL}/{cliente['id_cliente']}/comprobantes", headers=headers).status_code == 200
    assert client.post(URL, headers=headers, json={**NUEVO, "cuit": "20-31456789-8"}).status_code == 403
    assert client.get(f"{URL}/consulta-cuit", headers=headers, params={"cuit": NUEVO["cuit"]}).status_code == 403
    assert client.post(f"{URL}/{cliente['id_cliente']}/baja", headers=headers).status_code == 403


def test_sin_sesion(client):
    assert client.get(URL).status_code == 401
