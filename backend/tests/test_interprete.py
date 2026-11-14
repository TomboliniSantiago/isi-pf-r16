"""CUU-016 pasos 3-4: interpretación del texto de un comprobante y validaciones automáticas."""

from datetime import date

import pytest
from pdf_prueba import factura_arca, pdf_con_texto

from app.errors import ErrorNegocio
from app.ocr.interprete import interpretar, normalizar_importe, validar
from app.ocr.motor import Formato, MotorPdfTesseract, detectar_formato

EMPRESA = ("30-71458213-1", "Distribuidora Andina S.A.")


def _campos(lineas, confianza=1.0):
    resultado = interpretar("\n".join(lineas), confianza, *EMPRESA)
    return {n: c.valor for n, c in resultado.campos.items()}, resultado


def test_factura_de_compra_completa():
    valores, resultado = _campos(factura_arca())
    assert valores == {
        "cuit": "30-70123456-8",
        "razon_social": "Mayorista del Litoral S.A.",
        "tipo_comprobante": "Factura A",
        "punto_venta": "3",
        "numero_comprobante": "1520",
        "fecha_emision": "2026-11-05",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_otros_impuestos": "0.00",
        "importe_total": "1210.00",
    }
    assert resultado.validaciones == []
    assert all(c.confianza >= 0.8 for c in resultado.campos.values())


def test_factura_de_venta_toma_los_datos_del_cliente():
    """En una venta la empresa es la emisora: la contraparte es el receptor."""
    lineas = factura_arca(
        emisor=("Distribuidora Andina S.A.", "30714582131"), receptor=("Comercial Santa Fe SRL", "30712345671")
    )
    valores, _ = _campos(lineas)
    assert valores["cuit"] == "30-71234567-1" and valores["razon_social"] == "Comercial Santa Fe SRL"


@pytest.mark.parametrize(("codigo", "letra", "tipo"), [("06", "B", "Factura B"), ("11", "C", "Factura C")])
def test_tipo_por_codigo_de_arca(codigo, letra, tipo):
    valores, _ = _campos(factura_arca(codigo=codigo, letra=letra))
    assert valores["tipo_comprobante"] == tipo


def test_confianza_del_ocr_reduce_la_de_cada_campo():
    _, resultado = _campos(factura_arca(), confianza=0.6)
    assert resultado.campos["importe_total"].confianza == pytest.approx(0.57)


def test_texto_vacio_deja_campos_sin_valor_y_confianza_nula():  # 3.a
    _, resultado = _campos([""], confianza=None)
    assert all(c.confianza == 0 for c in resultado.campos.values())
    assert resultado.campos["cuit"].valor is None and resultado.campos["importe_total"].valor is None


def test_formato_alternativo_numero_y_total():
    lineas = [
        "FACTURA A",
        "Nro 0004-00000077",
        "Fecha 01/10/2026",
        "CUIT 30-70123456-8",
        "Neto Gravado 500,00",
        "IVA 21% 105,00",
        "TOTAL 605,00",
    ]
    valores, resultado = _campos(lineas)
    assert (valores["punto_venta"], valores["numero_comprobante"]) == ("4", "77")
    assert valores["importe_total"] == "605.00"
    assert resultado.campos["importe_total"].confianza < 0.8  # rótulo genérico: menor confianza


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("1.234.567,89", "1234567.89"),
        ("1234567,89", "1234567.89"),
        ("1,234,567.89", "1234567.89"),
        ("1234.5", "1234.50"),
        ("1.234", "1234.00"),
    ],
)
def test_normalizar_importe(texto, esperado):
    assert normalizar_importe(texto) == esperado


# ---------- Validaciones automáticas (paso 4 / 6.a) ----------


def _codigos(valores):
    return {v.codigo: v for v in validar(valores, hoy=date(2026, 11, 13))}


def test_aritmetica_inconsistente():
    v = _codigos(
        {
            "importe_neto_gravado": "1000.00",
            "importe_iva": "210.00",
            "importe_otros_impuestos": "0.00",
            "importe_total": "1200.00",
        }
    )
    assert v["aritmetica"].nivel == "error" and "diferencia 10.00" in v["aritmetica"].mensaje
    assert "importe_total" in v["aritmetica"].campos


def test_cuit_con_digito_verificador_invalido():
    assert _codigos({"cuit": "30-70123456-9"})["cuit"].nivel == "error"


def test_alicuota_no_habitual_es_advertencia():
    v = _codigos({"importe_neto_gravado": "1000.00", "importe_iva": "150.00", "importe_total": "1150.00"})
    assert v["alicuota"].nivel == "advertencia" and "aritmetica" not in v


def test_fecha_futura_es_advertencia():
    assert _codigos({"fecha_emision": "2026-12-31"})["fecha_futura"].nivel == "advertencia"


# ---------- Formato y lectura (2.a) ----------


def test_formato_por_contenido():
    assert detectar_formato(b"%PDF-1.4 ...") == Formato.PDF
    assert detectar_formato(b"\x89PNG\r\n\x1a\n...") == Formato.PNG
    assert detectar_formato(b"\xff\xd8\xff\xe0...") == Formato.JPG
    with pytest.raises(ErrorNegocio):
        detectar_formato(b"PK\x03\x04 un archivo zip")


def test_lectura_de_pdf_con_texto():
    lectura = MotorPdfTesseract().leer(pdf_con_texto(factura_arca()), Formato.PDF)
    assert lectura.motor == "pdf-texto" and lectura.confianza == 1.0 and "Importe Total" in lectura.texto


def test_pdf_danado():
    with pytest.raises(ErrorNegocio):
        MotorPdfTesseract().leer(b"%PDF-1.4 basura", Formato.PDF)
