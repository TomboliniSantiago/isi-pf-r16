"""CUU-016 Registrar comprobante con OCR/NLP: carga, revisión, corrección y registro."""

import pytest
from conftest import auditorias
from pdf_prueba import factura_arca, pdf_con_texto

from app import almacenamiento
from app.config import get_settings
from app.main import app
from app.models import (
    AsientoContable,
    Cliente,
    Compra,
    CuentaPredeterminada,
    Documento,
    DocumentoCampo,
    EmpresaEmisora,
    PlanCuenta,
    Proveedor,
    Rol,
    Venta,
)
from app.ocr.motor import TextoOcr, get_motor

URL = "/api/documentos"
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32


@pytest.fixture(autouse=True)
def carpeta(tmp_path, monkeypatch):
    monkeypatch.setattr(almacenamiento, "_raiz", lambda: tmp_path)
    return tmp_path


@pytest.fixture
def base(db):
    db.add(
        EmpresaEmisora(
            id_emisor=1,
            razon_social="Distribuidora Andina S.A.",
            cuit="30-71458213-1",
            condicion_iva="Responsable Inscripto",
        )
    )

    def cuenta(codigo, nombre, tipo, naturaleza):
        c = PlanCuenta(codigo=codigo, nombre=nombre, tipo_cuenta=tipo, imputable="1", activo="1", naturaleza=naturaleza)
        db.add(c)
        db.flush()
        return c.id_cuenta

    for clave, datos in {
        "COMPRAS": ("1.1.4.01", "Mercaderías", "ACTIVO", "DEUDORA"),
        "IVA_CREDITO_FISCAL": ("1.1.3.09", "IVA Crédito Fiscal", "ACTIVO", "DEUDORA"),
        "PROVEEDORES": ("2.1.1.01", "Proveedores", "PASIVO", "ACREEDORA"),
    }.items():
        db.add(CuentaPredeterminada(clave=clave, id_cuenta=cuenta(*datos)))
    proveedor = Proveedor(
        razon_social="Mayorista del Litoral S.A.",
        cuit="30-70123456-8",
        condicion_iva="Responsable Inscripto",
        activo="1",
    )
    cliente = Cliente(
        razon_social="Comercial Santa Fe SRL", cuit="30-71234567-1", condicion_iva="Responsable Inscripto", activo="1"
    )
    db.add_all([proveedor, cliente])
    db.commit()
    return {"proveedor": proveedor.id_proveedor, "cliente": cliente.id_cliente}


@pytest.fixture
def contador(crear_usuario, login):
    crear_usuario("contador@eugenia.com.ar", Rol.CONTADOR)
    return login("contador@eugenia.com.ar")


@pytest.fixture
def motor_simulado():
    """Reemplaza el OCR por uno que devuelve el texto y la confianza indicados."""

    def _usar(texto: str, confianza: float | None, aviso: str | None = None):
        class Simulado:
            def leer(self, contenido, formato):
                return TextoOcr(texto=texto, confianza=confianza, motor="simulado", aviso=aviso)

        app.dependency_overrides[get_motor] = Simulado

    yield _usar
    app.dependency_overrides.pop(get_motor, None)


def _cargar(client, headers, contenido, operacion="COMPRA", nombre="factura.pdf"):
    return client.post(URL, headers=headers, files={"archivo": (nombre, contenido)}, data={"operacion": operacion})


def _campos(documento):
    return {c["campo"]: c for c in documento["campos"]}


def _registro(base, **extra):
    datos = {
        "id_contraparte": base["proveedor"],
        "tipo_comprobante": "Factura A",
        "punto_venta": 3,
        "numero_comprobante": 1520,
        "fecha_emision": "2026-11-05",
        "condicion": "Cuenta Corriente",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_otros_impuestos": "0.00",
        "importe_total": "1210.00",
    }
    datos.update(extra)
    return datos


# ---------- Carga y extracción (pasos 1-5) ----------


def test_carga_de_factura_pdf_extrae_los_datos(client, db, contador, base, carpeta):
    pdf = pdf_con_texto(factura_arca())
    r = _cargar(client, contador, pdf)
    assert r.status_code == 201, r.text
    doc = r.json()
    assert doc["estado"] == "PENDIENTE_REVISION" and doc["motor_ocr"] == "pdf-texto"
    campos = _campos(doc)
    assert campos["cuit"]["valor_extraido"] == "30-70123456-8"
    assert campos["importe_total"]["valor_extraido"] == "1210.00"
    assert not any(c["requiere_revision"] for c in doc["campos"])
    assert doc["validaciones"] == []
    assert doc["contraparte_sugerida"]["id"] == base["proveedor"]  # paso 3 de CUU-002
    assert len(list(carpeta.rglob("*.pdf"))) == 1  # archivo original guardado
    assert client.get(f"{URL}/{doc['id_documento']}/archivo", headers=contador).content == pdf
    assert len(auditorias(db, "ALTA")) == 1


def test_formato_no_soportado(client, contador, base):  # 2.a
    r = _cargar(client, contador, b"PK\x03\x04 un zip", nombre="factura.zip")
    assert r.status_code == 422 and "PDF, PNG o JPG" in r.json()["detail"]


def test_archivo_vacio_o_demasiado_grande(client, contador, base, monkeypatch):
    assert _cargar(client, contador, b"").status_code == 422
    monkeypatch.setattr(get_settings(), "comprobante_max_mb", 0)
    assert _cargar(client, contador, pdf_con_texto(factura_arca())).status_code == 422


def test_mismo_archivo_dos_veces(client, contador, base):
    pdf = pdf_con_texto(factura_arca())
    primero = _cargar(client, contador, pdf).json()
    r = _cargar(client, contador, pdf)
    assert r.status_code == 409 and "ya fue cargado" in r.json()["detail"]
    client.post(f"{URL}/{primero['id_documento']}/descartar", headers=contador)
    assert _cargar(client, contador, pdf).status_code == 201


def test_imagen_sin_ocr_disponible_se_completa_a_mano(client, contador, base, motor_simulado):  # 3.a
    motor_simulado("", None, aviso="Tesseract no está instalado")
    doc = _cargar(client, contador, PNG, nombre="foto.png").json()
    assert doc["aviso_ocr"] == "Tesseract no está instalado" and doc["tipo_contenido"] == "image/png"
    assert all(c["requiere_revision"] for c in doc["campos"])
    r = client.post(
        f"{URL}/{doc['id_documento']}/registrar",
        headers=contador,
        json=_registro(base, campos_revisados=[c["campo"] for c in doc["campos"]]),
    )
    assert r.status_code == 200, r.text
    assert all(c["corregido"] for c in r.json()["campos"] if c["campo"] != "importe_otros_impuestos")


# ---------- Revisión obligatoria (4.a / 6.a) ----------


def test_baja_confianza_exige_revision(client, contador, base, motor_simulado):  # 4.a
    motor_simulado("\n".join(factura_arca()), 0.5)
    doc = _cargar(client, contador, PNG, nombre="foto.png").json()
    assert all(c["requiere_revision"] for c in doc["campos"])
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base))
    assert r.status_code == 422 and "Revise los campos marcados" in r.json()["detail"]

    revisados = [c["campo"] for c in doc["campos"]]
    r = client.post(
        f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base, campos_revisados=revisados)
    )
    assert r.status_code == 200, r.text
    assert all(c["revisado"] for c in r.json()["campos"])


def test_inconsistencia_aritmetica_exige_revisar_los_importes(client, contador, base):  # 6.a
    doc = _cargar(client, contador, pdf_con_texto(factura_arca(total="1.200,00"))).json()
    assert [v["codigo"] for v in doc["validaciones"]] == ["aritmetica"]
    campos = _campos(doc)
    assert campos["importe_total"]["requiere_revision"] and not campos["cuit"]["requiere_revision"]
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base))
    assert r.status_code == 422 and "Total" in r.json()["detail"]


# ---------- Registro (pasos 7-11) ----------


def test_registrar_crea_compra_pendiente_y_luego_se_contabiliza(client, db, contador, base):
    doc = _cargar(client, contador, pdf_con_texto(factura_arca())).json()
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base))
    assert r.status_code == 200, r.text
    registrado = r.json()
    assert registrado["estado"] == "REGISTRADO" and registrado["comprobante"]["tabla"] == "COMPRA"
    assert not any(c["corregido"] for c in registrado["campos"])
    id_compra = registrado["comprobante"]["id"]
    compra = client.get(f"/api/compras/{id_compra}", headers=contador).json()
    assert compra["estado"] == "PENDIENTE" and compra["asiento"] is None  # el OCR no contabiliza solo
    assert db.query(AsientoContable).count() == 0

    r = client.post(f"/api/compras/{id_compra}/contabilizar", headers=contador)
    assert r.status_code == 200 and r.json()["asiento"]["numero_asiento"] == 1
    # Trazabilidad: documento → compra → asiento
    asociados = client.get(URL, headers=contador, params={"tabla_asociada": "COMPRA", "id_registro": id_compra}).json()
    assert [d["id_documento"] for d in asociados] == [doc["id_documento"]]
    assert len(auditorias(db, "REGISTRO")) == 1


def test_correccion_conserva_el_valor_extraido_y_se_audita(client, db, contador, base):  # 7.a
    doc = _cargar(client, contador, pdf_con_texto(factura_arca(total="1.200,00"))).json()
    datos = _registro(
        base, campos_revisados=["importe_neto_gravado", "importe_iva", "importe_otros_impuestos", "importe_total"]
    )
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=datos)
    assert r.status_code == 200, r.text
    total = _campos(r.json())["importe_total"]
    assert total["valor_extraido"] == "1200.00" and total["valor_final"] == "1210.00" and total["corregido"]
    db.expire_all()
    guardado = db.query(DocumentoCampo).filter_by(campo="importe_total").one()
    assert guardado.valor_extraido == "1200.00" and guardado.valor_final == "1210.00"
    correccion = auditorias(db, "CORRECCION")
    assert (
        len(correccion) == 1 and "1200.00" in correccion[0].datos_anteriores and "1210.00" in correccion[0].datos_nuevos
    )


def test_registrar_venta(client, db, contador, base):
    lineas = factura_arca(
        emisor=("Distribuidora Andina S.A.", "30714582131"),
        receptor=("Comercial Santa Fe SRL", "30712345671"),
        punto_venta=1,
        numero=40,
    )
    doc = _cargar(client, contador, pdf_con_texto(lineas), operacion="VENTA").json()
    assert doc["contraparte_sugerida"]["id"] == base["cliente"]
    datos = _registro(base, id_contraparte=base["cliente"], punto_venta=1, numero_comprobante=40)
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=datos)
    assert r.status_code == 200, r.text
    assert r.json()["comprobante"]["tabla"] == "VENTA"
    assert db.query(Venta).one().estado == "PENDIENTE"


def test_comprobante_ya_registrado_no_se_duplica(client, db, contador, base):
    doc = _cargar(client, contador, pdf_con_texto(factura_arca())).json()
    client.post(
        "/api/compras",
        headers=contador,
        json={
            "id_proveedor": base["proveedor"],
            "tipo_comprobante": "Factura A",
            "punto_venta": 3,
            "numero_comprobante": 1520,
            "fecha_emision": "2026-11-05",
            "condicion_compra": "Cuenta Corriente",
            "importe_neto_gravado": "1000.00",
            "importe_iva": "210.00",
            "importe_total": "1210.00",
        },
    )
    r = client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base))
    assert r.status_code == 409 and "ya fue registrado" in r.json()["detail"]
    db.expire_all()
    assert db.query(Compra).count() == 1
    assert db.get(Documento, doc["id_documento"]).estado == "PENDIENTE_REVISION"


def test_descartar_es_baja_logica(client, db, contador, base):
    doc = _cargar(client, contador, pdf_con_texto(factura_arca())).json()
    r = client.post(f"{URL}/{doc['id_documento']}/descartar", headers=contador)
    assert r.status_code == 200 and r.json()["estado"] == "DESCARTADO"
    assert db.query(Documento).count() == 1
    assert (
        client.post(f"{URL}/{doc['id_documento']}/registrar", headers=contador, json=_registro(base)).status_code == 409
    )
    assert client.post(f"{URL}/{doc['id_documento']}/descartar", headers=contador).status_code == 409


# ---------- Permisos ----------


def test_consulta_no_carga_pero_puede_ver(client, crear_usuario, login, contador, base):
    doc = _cargar(client, contador, pdf_con_texto(factura_arca())).json()
    crear_usuario("consulta@eugenia.com.ar", Rol.CONSULTA)
    headers = login("consulta@eugenia.com.ar")
    assert _cargar(client, headers, pdf_con_texto(factura_arca(numero=2))).status_code == 403
    assert client.get(f"{URL}/{doc['id_documento']}", headers=headers).status_code == 200
    assert len(client.get(URL, headers=headers).json()) == 1


def test_sin_sesion(client, base):
    assert client.get(URL).status_code == 401
