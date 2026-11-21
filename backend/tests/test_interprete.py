"""CUU-016 pasos 3-4: interpretación del texto de un comprobante y validaciones automáticas."""

import io
from datetime import date

import pytest
from pdf_prueba import (
    factura_arca,
    factura_en_dolares,
    factura_preimpresa,
    pdf_con_texto,
    pdf_con_trazos,
    pdf_por_caracter,
)
from PIL import Image

from app.errors import ErrorNegocio
from app.ocr.interprete import interpretar, normalizar_cotizacion, normalizar_importe, validar
from app.ocr.motor import DPI_RENDERIZADO, Formato, MotorPdfTesseract, TextoOcr, detectar_formato

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
        "moneda": "ARS",
        "cotizacion": "1",
        "cae": "76451234567890",
        "cae_vencimiento": "2026-11-15",
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


def test_pdf_sin_texto_se_reconoce_la_pagina_renderizada(monkeypatch):
    """Lo dibujado como trazos (no solo las imágenes incrustadas) llega a Tesseract, a 300 dpi."""
    recibidas = []
    monkeypatch.setattr(
        MotorPdfTesseract,
        "_reconocer_imagenes",
        lambda self, imagenes: recibidas.extend(imagenes) or TextoOcr(texto="", confianza=None, motor="tesseract"),
    )
    MotorPdfTesseract().leer(pdf_con_trazos(), Formato.PDF)

    assert len(recibidas) == 1
    with Image.open(io.BytesIO(recibidas[0])) as pagina:
        escala = DPI_RENDERIZADO / 72
        ancho, alto = pagina.size
        assert abs(ancho - 595 * escala) <= 1 and abs(alto - 842 * escala) <= 1  # A4 a 300 dpi
        gris = pagina.convert("L")
        # El rectángulo (100..300 x 700..750 pt, origen abajo) se ve negro; fuera de él, blanco.
        assert gris.getpixel((round(200 * escala), round((842 - 725) * escala))) < 50
        assert gris.getpixel((round(400 * escala), round(400 * escala))) > 200


# ---------- PDF con un carácter por posición y facturas preimpresas ----------


def test_pdf_con_un_caracter_por_posicion_se_lee_por_renglones():
    lectura = MotorPdfTesseract().leer(pdf_por_caracter(factura_preimpresa()), Formato.PDF)
    lineas = lectura.texto.splitlines()
    assert lectura.motor == "pdf-texto" and lectura.confianza == 1.0
    assert "FACTURA" in lineas
    assert "Señor(es): DISTRIBUIDORA ANDINA S.A.   Cod. Cliente: 0ANDI" in lineas
    assert "TOTAL   1,210.00" in lineas


def test_pdf_normal_no_se_rearma_por_posicion():
    """La lectura estándar se mantiene para los PDF que ya traen el texto por renglones."""
    lectura = MotorPdfTesseract().leer(pdf_con_texto(factura_arca()), Formato.PDF)
    assert "Importe Neto Gravado: $ 1.000,00" in lectura.texto.splitlines()


def test_factura_preimpresa_completa():
    lectura = MotorPdfTesseract().leer(pdf_por_caracter(factura_preimpresa()), Formato.PDF)
    resultado = interpretar(lectura.texto, lectura.confianza, *EMPRESA)
    valores = {n: c.valor for n, c in resultado.campos.items()}
    assert valores == {
        "cuit": "30-70123456-8",
        "razon_social": None,  # el nombre del emisor no está en el texto
        "tipo_comprobante": "Factura A",
        "punto_venta": "12",
        "numero_comprobante": "4567",
        "fecha_emision": "2026-09-04",
        "importe_neto_gravado": "1000.00",
        "importe_iva": "210.00",
        "importe_otros_impuestos": "0.00",
        "importe_total": "1210.00",
        "moneda": "ARS",
        "cotizacion": "1",
        "cae": "76451234567890",
        "cae_vencimiento": "2026-09-14",
    }
    assert resultado.validaciones == []
    # Rótulos genéricos: el neto y el total quedan para revisar.
    assert resultado.campos["importe_neto_gravado"].confianza < 0.8
    assert resultado.campos["importe_total"].confianza < 0.8


@pytest.mark.parametrize(
    ("linea", "esperado"),
    [
        ("Fecha: 04/09/26", "2026-09-04"),
        ("Fecha: 04 / 09 / 2026", "2026-09-04"),
        ("Fecha Inicio Actividades: 15/05/1983\nEmitida el 02/10/2026", "2026-10-02"),
        ("Fecha de Vto. de CAE: 15/11/2026\nRecibido 01/11/2026", "2026-11-01"),
    ],
)
def test_fecha_de_emision(linea, esperado):
    valores, _ = _campos([linea])
    assert valores["fecha_emision"] == esperado


def test_solo_fecha_de_inicio_de_actividades_no_es_emision():
    valores, _ = _campos(["Fecha Inicio Actividades: 15/05/1983"])
    assert valores["fecha_emision"] is None


def test_subtotal_no_es_el_total():
    valores, _ = _campos(["SUB-TOTAL 1,000.00", "SUBTOTAL 1,000.00", "TOTAL 1,210.00"])
    assert valores["importe_total"] == "1210.00"


def test_iva_con_alicuota_sin_porcentaje_toma_el_importe():
    valores, resultado = _campos(["IVA : 10.50   105.00"])
    assert valores["importe_iva"] == "105.00"
    assert resultado.campos["importe_iva"].confianza == pytest.approx(0.85)


def test_neto_es_el_ultimo_subtotal():
    valores, _ = _campos(["SUB-TOTAL 1,050.00", "DESC. 50.00", "SUB-TOTAL 1,000.00"])
    assert valores["importe_neto_gravado"] == "1000.00"


def test_neto_gravado_tiene_prioridad_sobre_subtotal():
    valores, _ = _campos(["Subtotal: $ 1.500,00", "Importe Neto Gravado: $ 1.000,00"])
    assert valores["importe_neto_gravado"] == "1000.00"


# ---------- Rótulos de otros generadores de facturas electrónicas ----------


def test_fecha_emision_sin_de():
    valores, resultado = _campos(["Fecha Emisión: 18/11/2026", "Inicio de Actividad: 01/12/2020"])
    assert valores["fecha_emision"] == "2026-11-18"
    assert resultado.campos["fecha_emision"].confianza == pytest.approx(0.95)


def test_etiquetas_html_en_el_texto_se_ignoran():
    valores, _ = _campos(["<b>Razón social:</b> Comercial Norte S.R.L.", "CUIT: 30-70123456-8"])
    assert valores["razon_social"] == "Comercial Norte S.R.L."


def test_iva_nunca_toma_la_alicuota():
    """Rótulos en una columna y los importes en otra: el IVA queda vacío antes que con la alícuota."""
    valores, _ = _campos(["Importe IVA 10.5%", "Importe IVA 21%", "Importe Total $ 1210.00", "$ 1000.00", "$ 210.00"])
    assert valores["importe_iva"] is None


@pytest.mark.parametrize(
    ("linea", "punto", "numero"),
    [
        ("Comp. Nro: 2000-00423216", "2000", "423216"),
        ("FACTURA: 0006-00014511", "6", "14511"),
        ("Nº: 0023-00008908", "23", "8908"),
        ("Nº 00027-00079382", "27", "79382"),
    ],
)
def test_punto_de_venta_y_numero_con_rotulo(linea, punto, numero):
    valores, resultado = _campos([linea])
    assert (valores["punto_venta"], valores["numero_comprobante"]) == (punto, numero)
    assert resultado.campos["numero_comprobante"].confianza == pytest.approx(0.9)


def test_rotulos_de_otros_documentos_no_son_el_numero():
    valores, _ = _campos(["Ing. Brutos Nº: 021-013864-9", "C.U.I.T. Nº: 30-70702485-9"])
    assert valores["punto_venta"] is None and valores["numero_comprobante"] is None


# ---------- Facturas B y C: el IVA según la operación ----------


def _factura_b(**extra):
    lineas = factura_arca(codigo="06", letra="B", neto="1.210,00", iva="0,00", total="1.210,00", **extra)
    return [linea for linea in lineas if not linea.startswith(("Importe Neto", "IVA 21%"))]


def _interpretar(lineas, operacion):
    resultado = interpretar("\n".join(lineas), 1.0, *EMPRESA, operacion)
    return {n: c.valor for n, c in resultado.campos.items()}, resultado


def test_compra_b_iva_cero_y_neto_igual_al_total():
    lineas = [*_factura_b(), "Régimen de Transparencia Fiscal al Consumidor (Ley 27.743)", "IVA Contenido: $ 210,00"]
    valores, resultado = _interpretar(lineas, "COMPRA")
    assert (valores["importe_neto_gravado"], valores["importe_iva"]) == ("1210.00", "0.00")
    assert resultado.validaciones == []
    assert resultado.campos["importe_neto_gravado"].confianza >= 0.8


def test_venta_b_toma_el_iva_contenido():
    valores, resultado = _interpretar([*_factura_b(), "IVA Contenido: ARS$ 210,00"], "VENTA")
    assert (valores["importe_neto_gravado"], valores["importe_iva"]) == ("1000.00", "210.00")
    assert resultado.validaciones == []


def test_venta_b_sin_iva_contenido_deja_neto_e_iva_para_completar():
    valores, resultado = _interpretar(_factura_b(), "VENTA")
    assert valores["importe_neto_gravado"] is None and valores["importe_iva"] is None
    assert resultado.campos["importe_iva"].confianza == 0


@pytest.mark.parametrize("operacion", ["COMPRA", "VENTA"])
def test_factura_c_iva_cero(operacion):
    lineas = factura_arca(codigo="11", letra="C", neto="500,00", iva="0,00", total="500,00")
    valores, _ = _interpretar(lineas, operacion)
    assert (valores["importe_neto_gravado"], valores["importe_iva"]) == ("500.00", "0.00")


def test_factura_a_no_cambia_con_la_operacion():
    assert _interpretar(factura_arca(), "COMPRA")[0] == _interpretar(factura_arca(), None)[0]


def test_sin_tipo_reconocido_no_se_aplica_la_regla():
    lineas = [linea for linea in _factura_b() if linea not in ("B", "FACTURA COD. 06")]
    valores, _ = _interpretar(lineas, "COMPRA")
    assert valores["tipo_comprobante"] is None and valores["importe_iva"] is None


# ---------- Moneda extranjera (modelo de la empresa piloto) ----------


def test_factura_en_dolares_completa():
    """Venta de la empresa: la contraparte es el cliente, sin el código interno delante del nombre."""
    resultado = interpretar("\n".join(factura_en_dolares()), 1.0, *EMPRESA, "VENTA")
    valores = {n: c.valor for n, c in resultado.campos.items()}
    assert valores == {
        "cuit": "30-71234567-1",
        "razon_social": "Comercial Santa Fe SRL",
        "tipo_comprobante": "Factura A",
        "punto_venta": "3",
        "numero_comprobante": "4512",
        "fecha_emision": "2026-11-05",
        "importe_neto_gravado": "28172.00",
        "importe_iva": "5916.12",
        "importe_otros_impuestos": "0.00",
        "importe_total": "34088.12",
        "moneda": "USD",
        "cotizacion": "1545.5",
        "cae": "86440858279262",
        "cae_vencimiento": "2026-11-15",
    }
    assert resultado.validaciones == []
    assert all(c.confianza >= 0.8 for c in resultado.campos.values())


def test_encabezado_iva_de_la_tabla_no_toma_el_renglon_siguiente():
    valores, _ = _campos(["Subtotal   Alicuota", "   IVA", "88497899  PRODUCTO   400.00"])
    assert valores["importe_iva"] is None


@pytest.mark.parametrize(
    ("lineas", "moneda", "cotizacion", "confianza"),
    [
        (["Importe Total: $ 100,00"], "ARS", "1", 0.85),
        (["Moneda: Pesos Argentinos"], "ARS", "1", 0.95),
        (["Importes expresados en: Dólares", "Cotización: $ 1.545,50"], "USD", "1545.5", 0.95),
        (["Moneda: EUR", "Cotización: 1680,2575"], "EUR", "1680.2575", 0.95),
        (["Importe Total: u$s 100.00", "tipo de cambio consignado de 1,545.50"], "USD", "1545.5", 0.8),
        (["TOTAL FOB: USD$ 20.66"], "USD", None, 0.8),
        (["SUBTOTAL US$ 50.00"], "USD", None, 0.8),
        # Dólares solo en la descripción de una factura en pesos: no definen la moneda.
        (
            ["Equivalente al 0.025% de VN u$s 35.903.000,-", "u$s 8.975.75 TC divisa 1.516,-", "TOTAL 13,607,237.00"],
            "ARS",
            "1",
            0.85,
        ),
    ],
)
def test_moneda_y_cotizacion(lineas, moneda, cotizacion, confianza):
    valores, resultado = _campos(lineas)
    assert (valores["moneda"], valores["cotizacion"]) == (moneda, cotizacion)
    assert resultado.campos["moneda"].confianza == pytest.approx(confianza)


def test_moneda_extranjera_sin_cotizacion_es_error():
    valores, resultado = _campos(["Moneda: Dólar", "Importe Total: u$s 100.00"])
    assert valores["moneda"] == "USD" and valores["cotizacion"] is None
    error = next(v for v in resultado.validaciones if v.codigo == "cotizacion")
    assert error.nivel == "error" and error.campos == ["moneda", "cotizacion"]


def test_moneda_no_admitida_es_error():
    assert {v.codigo for v in validar({"moneda": "BRL"})} == {"moneda"}


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("1,545.50", "1545.5"), ("1.545,50", "1545.5"), ("1680,2575", "1680.2575"), ("0", None), ("abc", None)],
)
def test_normalizar_cotizacion(texto, esperado):
    assert normalizar_cotizacion(texto) == esperado


def test_lectura_por_posicion_junta_rotulos_e_importes():
    """Rótulos e importes escritos por separado (como Microsoft Print to PDF) quedan en el mismo renglón."""
    lectura = MotorPdfTesseract().leer(pdf_por_caracter(factura_en_dolares()), Formato.PDF)
    assert "Importe Total: u$s   34,088.12" in lectura.texto.splitlines()


# ---------- CAE y vencimiento (CUU-017) ----------


@pytest.mark.parametrize(
    ("lineas", "cae", "vencimiento", "confianza"),
    [
        (["CAE N°: 76451234567890", "Fecha de Vto. de CAE: 15/11/2026"], "76451234567890", "2026-11-15", 0.95),
        (["C.A.E. : 86394530356192", "VENCIMIENTO : 24/09/2026"], "86394530356192", "2026-09-24", 0.85),
        (["CAE: 76451234567890   Vto: 14/09/26"], "76451234567890", "2026-09-14", 0.85),
        # Un vencimiento de pago no es el del CAE.
        (["CAE: 76451234567890", "Total 1.210,00", "Vencimiento de Pago: 05/11/2026"], "76451234567890", None, 0.0),
        # Sin 14 dígitos no hay CAE.
        (["CAE: 7645123456789"], None, None, 0.0),
        # Rótulos y valores en columnas separadas: el único número suelto de 14 dígitos y la fecha del renglón
        # siguiente (el código de barras, más largo, no cuenta).
        (
            [
                "3071693224506200086463286812823202611184",
                "Área de CAE Nro.:",
                "Defensa del Consumidor: 147   86463286812823",
                "Fecha Vto. CAE:",
                "Orientación al Consumidor 148   28/11/2026",
            ],
            "86463286812823",
            "2026-11-28",
            0.7,
        ),
    ],
)
def test_cae_y_vencimiento(lineas, cae, vencimiento, confianza):
    valores, resultado = _campos(lineas)
    assert (valores["cae"], valores["cae_vencimiento"]) == (cae, vencimiento)
    assert resultado.campos["cae_vencimiento"].confianza == pytest.approx(confianza)


def test_vencimiento_del_cae_invalido_es_error():
    valores, resultado = _campos(["CAE: 76451234567890", "Fecha de Vto. de CAE: 31/02/2026"])
    assert valores["cae_vencimiento"] == "31/02/2026"
    assert [v.codigo for v in resultado.validaciones] == ["cae_vencimiento"]


def test_cae_sin_rotulo_al_lado_tiene_confianza_baja():
    valores, resultado = _campos(["C.A.E.", "Total 1.210,00", "86394530356192", "CBU 0070339820000018207059"])
    assert valores["cae"] == "86394530356192"
    assert resultado.campos["cae"].confianza == pytest.approx(0.6)


def test_dos_numeros_sueltos_de_14_digitos_no_definen_el_cae():
    valores, _ = _campos(["C.A.E.", "Total 1.210,00", "86394530356192", "12345678901234"])
    assert valores["cae"] is None
