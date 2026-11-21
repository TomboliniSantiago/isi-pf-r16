"""CUU-017 Validar comprobante con ARCA (ventas y compras), con el simulador de ARCA."""

import json
from datetime import timedelta

import pytest
from conftest import auditorias

from app.arca.comprobantes import (
    CAE_ERROR_SERVICIO,
    CAE_INEXISTENTE,
    CAE_SIN_RESPUESTA,
    CAE_TOTAL_DISTINTO,
    CAE_VENCIDO,
    get_servicio_comprobantes,
)
from app.main import app
from app.models import Cliente, Compra, EmpresaEmisora, EstadoFiscal, Proveedor, Rol, ValidacionArca
from app.tiempo import ahora

CAE = "76123456789012"
EMPRESA = "30-71458213-1"
PROVEEDOR = "30-70123456-8"


@pytest.fixture
def base(db):
    db.add(
        EmpresaEmisora(
            id_emisor=1, razon_social="Distribuidora Andina S.A.", cuit=EMPRESA, condicion_iva="Responsable Inscripto"
        )
    )
    proveedor = Proveedor(
        razon_social="Mayorista del Litoral S.A.", cuit=PROVEEDOR, condicion_iva="Responsable Inscripto", activo="1"
    )
    cliente = Cliente(razon_social="Comercial Santa Fe S.R.L.", cuit="30-71234567-1", activo="1")
    db.add_all([proveedor, cliente])
    db.commit()
    return {"proveedor": proveedor.id_proveedor, "cliente": cliente.id_cliente}


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


def _compra(client, contador, base, **extra):
    datos = {
        "id_proveedor": base["proveedor"],
        "tipo_comprobante": "Factura A",
        "punto_venta": 3,
        "numero_comprobante": 1520,
        "fecha_emision": "2026-11-05",
        "condicion_compra": "Cuenta Corriente",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_total": "1210.00",
        "cae": CAE,
        **extra,
    }
    r = client.post("/api/compras", headers=contador, json=datos)
    assert r.status_code == 201, r.text
    return r.json()


def _venta(client, contador, base, **extra):
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
        "cae": CAE,
        **extra,
    }
    r = client.post("/api/ventas", headers=contador, json=datos)
    assert r.status_code == 201, r.text
    return r.json()


def _validar(client, contador, compra):
    return client.post(f"/api/compras/{compra['id_compra']}/validar-arca", headers=contador)


def _estado_fiscal(client, contador, compra):
    return client.get(f"/api/compras/{compra['id_compra']}", headers=contador).json()["estado_fiscal"]


# ---------- Camino básico (pasos 1-8) ----------


def test_compra_valida(client, db, contador, base):
    compra = _compra(client, contador, base)
    assert compra["estado_fiscal"] == "PENDIENTE" and compra["cae"] == CAE

    r = _validar(client, contador, compra)
    assert r.status_code == 200, r.text
    resultado = r.json()
    assert resultado["estado"] == "VALIDO" and resultado["diferencias"] == []
    assert resultado["usuario"] == "contador@eugenia.com.ar" and resultado["fecha_respuesta"]
    assert resultado["cae_vencimiento_arca"] == "2026-11-15"

    actual = client.get(f"/api/compras/{compra['id_compra']}", headers=contador).json()
    # El vencimiento del CAE se completa con el que informó ARCA; el estado contable no cambia.
    assert actual["estado_fiscal"] == "VALIDO" and actual["cae_vencimiento"] == "2026-11-15"
    assert actual["estado"] == "PENDIENTE"

    # En una compra, el emisor es el proveedor y el receptor, la empresa.
    validacion = db.query(ValidacionArca).one()
    enviado = json.loads(validacion.consulta)
    assert enviado["CuitEmisor"] == PROVEEDOR and enviado["DocNroReceptor"] == EMPRESA
    assert enviado["CbteTipo"] == 1 and enviado["CodAutorizacion"] == CAE and enviado["ImpTotal"] == "1210.00"

    (registro,) = auditorias(db, "VALIDACION_ARCA")
    assert registro.tabla_afectada == "COMPRA" and registro.id_registro_afectado == compra["id_compra"]
    assert json.loads(registro.datos_anteriores) == {"estado_fiscal": "PENDIENTE"}
    assert json.loads(registro.datos_nuevos)["estado_fiscal"] == "VALIDO"


def test_venta_valida_con_la_empresa_como_emisor(client, db, contador, base):
    venta = _venta(client, contador, base)
    r = client.post(f"/api/ventas/{venta['id_venta']}/validar-arca", headers=contador)
    assert r.status_code == 200 and r.json()["estado"] == "VALIDO"
    assert json.loads(db.query(ValidacionArca).one().consulta)["CuitEmisor"] == EMPRESA

    actual = client.get(f"/api/ventas/{venta['id_venta']}", headers=contador).json()
    assert actual["estado_fiscal"] == "VALIDO"
    historial = client.get(f"/api/ventas/{venta['id_venta']}/validaciones", headers=contador).json()
    assert [v["estado"] for v in historial] == ["VALIDO"]


# ---------- Caminos alternativos ----------


@pytest.mark.parametrize(
    ("cae", "estado", "mensaje"),
    [
        (CAE_SIN_RESPUESTA, "ERROR_INTEGRACION", "No fue posible establecer conexión con ARCA"),  # 3.a
        (CAE_ERROR_SERVICIO, "ERROR_INTEGRACION", "ARCA respondió con un error"),  # 3.a
        (CAE_INEXISTENTE, "INVALIDO", "ARCA informa que el comprobante no existe"),  # 4.a
        (CAE_VENCIDO, "OBSERVADO", "El CAE venció el 04/11/2026"),  # 5.a
    ],
)
def test_caminos_alternativos(client, contador, base, cae, estado, mensaje):
    compra = _compra(client, contador, base, cae=cae)
    r = _validar(client, contador, compra)
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == estado and mensaje in r.json()["mensaje"]
    assert _estado_fiscal(client, contador, compra) == estado


def test_datos_distintos_quedan_pendientes_de_auditoria(client, contador, base):  # 6.a
    compra = _compra(client, contador, base, cae=CAE_TOTAL_DISTINTO)
    resultado = _validar(client, contador, compra).json()
    assert resultado["estado"] == "PENDIENTE_AUDITORIA"
    assert resultado["diferencias"] == [
        {"campo": "importe_total", "etiqueta": "Importe total", "registrado": "1210.00", "arca": "1310.00"}
    ]
    # Con diferencias, el vencimiento del CAE no se toma de ARCA.
    actual = client.get(f"/api/compras/{compra['id_compra']}", headers=contador).json()
    assert actual["estado_fiscal"] == "PENDIENTE_AUDITORIA" and actual["cae_vencimiento"] is None


def test_vencimiento_del_cae_distinto_al_registrado(client, contador, base):  # 6.a
    compra = _compra(client, contador, base, cae_vencimiento="2026-11-20")
    resultado = _validar(client, contador, compra).json()
    assert resultado["estado"] == "PENDIENTE_AUDITORIA"
    assert resultado["diferencias"][0]["campo"] == "cae_vencimiento"
    assert resultado["diferencias"][0]["arca"] == "15/11/2026"


def test_reintento_despues_de_un_error_de_integracion(client, contador, base):  # 3.a
    compra = _compra(client, contador, base, cae=CAE_SIN_RESPUESTA)
    assert _validar(client, contador, compra).json()["estado"] == "ERROR_INTEGRACION"

    # El usuario corrige el CAE (la compra sigue pendiente) y vuelve a validar.
    datos = {**_datos_compra(compra), "cae": CAE}
    r = client.put(f"/api/compras/{compra['id_compra']}", headers=contador, json=datos)
    assert r.status_code == 200 and r.json()["estado_fiscal"] == "PENDIENTE"
    assert _validar(client, contador, compra).json()["estado"] == "VALIDO"

    historial = client.get(f"/api/compras/{compra['id_compra']}/validaciones", headers=contador).json()
    assert [v["estado"] for v in historial] == ["VALIDO", "ERROR_INTEGRACION"]


def test_modificar_sin_cambiar_datos_fiscales_conserva_la_validacion(client, contador, base):
    """La validación no condiciona la contabilización, y contabilizar desde la revisión del asiento (PUT con la
    condición de pago u otras cuentas) no la invalida."""
    compra = _compra(client, contador, base)
    assert _validar(client, contador, compra).json()["estado"] == "VALIDO"
    datos = {**_datos_compra(compra), "condicion_compra": "Contado", "cae_vencimiento": "2026-11-15"}
    r = client.put(f"/api/compras/{compra['id_compra']}", headers=contador, json=datos)
    assert r.status_code == 200 and r.json()["estado_fiscal"] == "VALIDO"


@pytest.mark.parametrize(
    "cambio", [{"importe_total": "1300.00", "importe_neto_gravado": "1090.00"}, {"fecha_emision": "2026-11-06"}]
)
def test_modificar_datos_fiscales_vuelve_a_pendiente(client, contador, base, cambio):
    compra = _compra(client, contador, base)
    _validar(client, contador, compra)
    datos = {**_datos_compra(compra), "cae_vencimiento": "2026-11-15", **cambio}
    r = client.put(f"/api/compras/{compra['id_compra']}", headers=contador, json=datos)
    assert r.status_code == 200 and r.json()["estado_fiscal"] == "PENDIENTE"


def test_falla_inesperada_del_adaptador_es_error_de_integracion(client, contador, base):  # 3.a
    class Roto:
        def consultar(self, consulta):
            raise RuntimeError("certificado vencido")

    compra = _compra(client, contador, base)
    app.dependency_overrides[get_servicio_comprobantes] = Roto
    try:
        resultado = _validar(client, contador, compra).json()
    finally:
        app.dependency_overrides.pop(get_servicio_comprobantes)
    assert resultado["estado"] == "ERROR_INTEGRACION" and "Error inesperado" in resultado["mensaje"]


# ---------- Precondiciones y reintento controlado ----------


def test_sin_cae_no_se_valida(client, contador, base):
    compra = _compra(client, contador, base, cae=None)
    r = _validar(client, contador, compra)
    assert r.status_code == 422 and "cargue primero su CAE" in r.json()["detail"]


@pytest.mark.parametrize("cae", ["123", "7612345678901A", "761234567890123"])
def test_cae_con_formato_invalido(client, contador, base, cae):
    datos = {
        "id_proveedor": base["proveedor"],
        "tipo_comprobante": "Factura A",
        "punto_venta": 3,
        "numero_comprobante": 1520,
        "fecha_emision": "2026-11-05",
        "condicion_compra": "Cuenta Corriente",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_total": "1210.00",
        "cae": cae,
    }
    assert client.post("/api/compras", headers=contador, json=datos).status_code == 422


def test_anulada_no_se_valida(client, contador, base):
    compra = _compra(client, contador, base)
    client.post(f"/api/compras/{compra['id_compra']}/anular", headers=contador)
    r = _validar(client, contador, compra)
    assert r.status_code == 409 and "anulada" in r.json()["detail"]


def test_comprobante_inexistente(client, contador, base):
    r = client.post("/api/compras/999/validar-arca", headers=contador)
    assert r.status_code == 404


def test_consulta_en_curso_no_se_duplica(client, db, contador, base):
    compra = _compra(client, contador, base)
    _en_curso(db, compra["id_compra"], ahora())
    r = _validar(client, contador, compra)
    assert r.status_code == 409 and "ya se está validando" in r.json()["detail"]


def test_consulta_interrumpida_se_puede_reintentar(client, db, contador, base):
    compra = _compra(client, contador, base)
    _en_curso(db, compra["id_compra"], ahora() - timedelta(minutes=10))
    assert _validar(client, contador, compra).json()["estado"] == "VALIDO"

    historial = client.get(f"/api/compras/{compra['id_compra']}/validaciones", headers=contador).json()
    assert [v["estado"] for v in historial] == ["VALIDO", "ERROR_INTEGRACION"]
    assert "se interrumpió" in historial[1]["mensaje"]


def test_permisos(client, crear_usuario, login, contador, base):
    compra = _compra(client, contador, base)
    crear_usuario("consulta@eugenia.com.ar", Rol.CONSULTA)
    consulta = login("consulta@eugenia.com.ar")
    assert _validar(client, consulta, compra).status_code == 403
    r = client.get(f"/api/compras/{compra['id_compra']}/validaciones", headers=consulta)
    assert r.status_code == 200 and r.json() == []


# ---------- Auxiliares ----------


def _datos_compra(compra):
    return {
        "id_proveedor": compra["proveedor"]["id_proveedor"],
        "tipo_comprobante": compra["tipo_comprobante"],
        "punto_venta": compra["punto_venta"],
        "numero_comprobante": compra["numero_comprobante"],
        "fecha_emision": compra["fecha_emision"],
        "condicion_compra": compra["condicion_compra"],
        "importe_neto_gravado": compra["importe_neto_gravado"],
        "importe_iva": compra["importe_iva"],
        "importe_total": compra["importe_total"],
        "cae": compra["cae"],
    }


def _en_curso(db, id_compra, inicio):
    """Simula una consulta a ARCA en curso (o que quedó sin respuesta) iniciada en `inicio`."""
    compra = db.get(Compra, id_compra)
    compra.estado_fiscal = EstadoFiscal.EN_VALIDACION
    db.add(
        ValidacionArca(
            tabla_comprobante="COMPRA",
            id_comprobante=id_compra,
            id_usuario=1,
            fecha_inicio=inicio,
            estado=EstadoFiscal.EN_VALIDACION,
        )
    )
    db.commit()
