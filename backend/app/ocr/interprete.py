"""Interpretación del texto de un comprobante (CUU-016 pasos 3-4).

Reconoce los campos de una factura argentina buscando sus rótulos habituales (los de la factura electrónica
de ARCA: "Punto de Venta", "Comp. Nro", "Fecha de Emisión", "CUIT", "Razón Social", "Importe Neto
Gravado", "IVA 21%", "Importe Otros Tributos", "Importe Total", "COD. 01"...). Cada campo lleva una
confianza (0 a 1): la del patrón que lo encontró multiplicada por la del OCR. Un campo no encontrado queda
vacío con confianza 0 (3.a).

La contraparte se distingue de la empresa por exclusión: en una compra, el CUIT y la razón social que no
son los de la empresa emisora son los del proveedor; en una venta, los del cliente.

Validaciones automáticas (paso 4 / 6.a): formato de punto de venta y número, fecha, dígito verificador del
CUIT, alícuota de IVA habitual y neto + IVA + otros tributos = total.
"""

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from app.cuit import digito_verificador

CAMPOS = (
    "cuit",
    "razon_social",
    "tipo_comprobante",
    "punto_venta",
    "numero_comprobante",
    "fecha_emision",
    "importe_neto_gravado",
    "importe_iva",
    "importe_otros_impuestos",
    "importe_total",
)
ETIQUETAS = {
    "cuit": "CUIT",
    "razon_social": "Razón social",
    "tipo_comprobante": "Tipo de comprobante",
    "punto_venta": "Punto de venta",
    "numero_comprobante": "Número",
    "fecha_emision": "Fecha de emisión",
    "importe_neto_gravado": "Neto gravado",
    "importe_iva": "IVA",
    "importe_otros_impuestos": "Otros impuestos",
    "importe_total": "Total",
}
IMPORTES = ("importe_neto_gravado", "importe_iva", "importe_otros_impuestos", "importe_total")
# Códigos de comprobante de ARCA: 1 Factura A, 6 Factura B, 11 Factura C.
CODIGOS_FACTURA = {1: "Factura A", 6: "Factura B", 11: "Factura C"}
ALICUOTAS_IVA = (Decimal("0"), Decimal("0.025"), Decimal("0.05"), Decimal("0.105"), Decimal("0.21"), Decimal("0.27"))
CENTAVO = Decimal("0.01")

_IMPORTE = r"\$?\s*(-?[\d.,]*\d)"


@dataclass
class Campo:
    valor: str | None
    confianza: float


@dataclass
class Validacion:
    codigo: str
    mensaje: str
    campos: list[str]
    # error: impide registrar sin corregir o revisar (6.a); advertencia: informativa.
    nivel: str = "error"


@dataclass
class Interpretacion:
    campos: dict[str, Campo]
    validaciones: list[Validacion] = field(default_factory=list)


def interpretar(
    texto: str, confianza_ocr: float | None, cuit_empresa: str | None, razon_social_empresa: str | None
) -> Interpretacion:
    factor = confianza_ocr if confianza_ocr is not None else 0.0
    plano = texto or ""
    encontrados: dict[str, tuple[str | None, float]] = {
        "cuit": _cuit(plano, cuit_empresa),
        "razon_social": _razon_social(plano, razon_social_empresa),
        "tipo_comprobante": _tipo(plano),
        **_punto_y_numero(plano),
        "fecha_emision": _fecha(plano),
        "importe_neto_gravado": _importe(plano, [r"(?:Importe\s+)?Neto\s+Gravado"], 0.95),
        "importe_iva": _iva(plano),
        "importe_otros_impuestos": _otros(plano),
        "importe_total": _total(plano),
    }
    campos = {
        nombre: Campo(valor, round(conf * factor, 4) if valor is not None else 0.0)
        for nombre, (valor, conf) in encontrados.items()
    }
    return Interpretacion(campos=campos, validaciones=validar({n: c.valor for n, c in campos.items()}))


# ---------- Validaciones (paso 4 / 6.a) ----------


def validar(valores: dict[str, str | None], hoy: date | None = None) -> list[Validacion]:
    resultado: list[Validacion] = []
    cuit = valores.get("cuit")
    if cuit and not cuit_valido(cuit):
        resultado.append(Validacion("cuit", f"El CUIT {cuit} no tiene un dígito verificador válido.", ["cuit"]))

    for campo, maximo, nombre in (("punto_venta", 99999, "punto de venta"), ("numero_comprobante", 99999999, "número")):
        valor = valores.get(campo)
        if valor and not (valor.isdigit() and 1 <= int(valor) <= maximo):
            resultado.append(
                Validacion(f"formato_{campo}", f"El {nombre} {valor} no tiene un formato válido.", [campo])
            )

    fecha = valores.get("fecha_emision")
    if fecha:
        try:
            emision = date.fromisoformat(fecha)
        except ValueError:
            resultado.append(Validacion("fecha", f"La fecha {fecha} no es válida.", ["fecha_emision"]))
        else:
            if emision > (hoy or date.today()):
                resultado.append(
                    Validacion(
                        "fecha_futura", "La fecha de emisión es posterior a hoy.", ["fecha_emision"], "advertencia"
                    )
                )

    importes = {c: a_decimal(valores.get(c)) for c in IMPORTES}
    neto, iva, otros, total = (importes[c] for c in IMPORTES)
    if neto is not None and iva is not None and total is not None:
        suma = neto + iva + (otros or Decimal("0"))
        if suma != total:
            resultado.append(
                Validacion(
                    "aritmetica",
                    f"Neto + IVA + otros impuestos ({suma:.2f}) no coincide con el total ({total:.2f}): "
                    f"diferencia {abs(total - suma):.2f}.",
                    list(IMPORTES),
                )
            )
    if neto and iva is not None and neto > 0:
        alicuota = iva / neto
        if all(abs(alicuota - a) > Decimal("0.005") for a in ALICUOTAS_IVA):
            resultado.append(
                Validacion(
                    "alicuota",
                    f"El IVA equivale al {alicuota * 100:.2f}% del neto, que no es una alícuota habitual "
                    "(21%, 10,5%, 27%, 5%, 2,5%).",
                    ["importe_neto_gravado", "importe_iva"],
                    "advertencia",
                )
            )
    return resultado


def cuit_valido(cuit: str) -> bool:
    digitos = re.sub(r"\D", "", cuit)
    return len(digitos) == 11 and digito_verificador(digitos[:10]) == int(digitos[10])


def a_decimal(valor: str | None) -> Decimal | None:
    if valor is None or valor == "":
        return None
    try:
        return Decimal(valor).quantize(CENTAVO)
    except InvalidOperation:
        return None


def normalizar_importe(texto: str) -> str | None:
    """'1.234.567,89' / '1234567,89' / '1,234,567.89' / '1234567.89' → '1234567.89'."""
    t = texto.strip().replace(" ", "")
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".") if t.rfind(",") > t.rfind(".") else t.replace(",", "")
    elif "," in t:
        t = t.replace(".", "").replace(",", ".") if t.count(",") == 1 else t.replace(",", "")
    elif t.count(".") > 1 or (t.count(".") == 1 and len(t.split(".")[1]) == 3):
        t = t.replace(".", "")
    valor = a_decimal(t)
    return f"{valor:.2f}" if valor is not None else None


# ---------- Reconocimiento de cada campo: (valor, confianza del patrón) ----------


def _primero(texto: str, patrones: list[tuple[str, float]]) -> tuple[re.Match[str] | None, float]:
    for patron, confianza in patrones:
        coincidencia = re.search(patron, texto, re.IGNORECASE)
        if coincidencia:
            return coincidencia, confianza
    return None, 0.0


def _cuit(texto: str, cuit_empresa: str | None) -> tuple[str | None, float]:
    propio = re.sub(r"\D", "", cuit_empresa or "")
    candidatos: list[str] = []
    for m in re.finditer(r"(?<!\d)(\d{2})[-\s]?(\d{8})[-\s]?(\d)(?!\d)", texto):
        digitos = "".join(m.groups())
        if digitos != propio and digitos not in candidatos:
            candidatos.append(digitos)
    if not candidatos:
        return None, 0.0
    validos = [c for c in candidatos if cuit_valido(c)]
    elegido = validos[0] if validos else candidatos[0]
    confianza = (0.95 if len(validos) == 1 else 0.7) if validos else 0.3
    return f"{elegido[:2]}-{elegido[2:10]}-{elegido[10]}", confianza


def _razon_social(texto: str, razon_social_empresa: str | None) -> tuple[str | None, float]:
    propia = (razon_social_empresa or "").strip().lower()
    for m in re.finditer(r"Raz[oó]n\s+Social\s*:?[ \t]*([^\n]+)", texto, re.IGNORECASE):
        valor = re.split(r"\s{2,}|\s+(?:Domicilio|CUIT|Fecha|Condici[oó]n)\b", m.group(1).strip(), maxsplit=1)[0]
        valor = valor.strip(" :-")
        if valor and valor.lower() != propia:
            return valor[:255], 0.8
    return None, 0.0


def _tipo(texto: str) -> tuple[str | None, float]:
    m, confianza = _primero(texto, [(r"C[oó]d(?:igo)?\.?\s*:?\s*0*(\d{1,3})\b", 0.95)])
    if m and int(m.group(1)) in CODIGOS_FACTURA:
        return CODIGOS_FACTURA[int(m.group(1))], confianza
    m, confianza = _primero(texto, [(r"FACTURA\s*\n?\s*\"?([ABC])\b", 0.85), (r"\b([ABC])\s*\n\s*FACTURA\b", 0.7)])
    return (f"Factura {m.group(1).upper()}", confianza) if m else (None, 0.0)


def _punto_y_numero(texto: str) -> dict[str, tuple[str | None, float]]:
    pv, conf_pv = _primero(texto, [(r"Punto\s+de\s+Venta\s*:?\s*(\d{1,5})\b", 0.95)])
    nro, conf_nro = _primero(texto, [(r"Comp(?:robante)?\.?\s*N(?:ro|°|º|o)\.?\s*:?\s*(\d{1,8})\b", 0.95)])
    if not (pv and nro):
        junto = re.search(r"(?<!\d)(\d{4,5})\s*-\s*(\d{8})(?!\d)", texto)
        if junto:
            return {
                "punto_venta": (str(int(junto.group(1))), 0.75),
                "numero_comprobante": (str(int(junto.group(2))), 0.75),
            }
    return {
        "punto_venta": (str(int(pv.group(1))), conf_pv) if pv else (None, 0.0),
        "numero_comprobante": (str(int(nro.group(1))), conf_nro) if nro else (None, 0.0),
    }


def _fecha(texto: str) -> tuple[str | None, float]:
    m, confianza = _primero(
        texto,
        [(r"Fecha\s+de\s+Emisi[oó]n\s*:?\s*(\d{1,2}[/.-]\d{1,2}[/.-]\d{4})", 0.95), (r"(\d{1,2}/\d{1,2}/\d{4})", 0.6)],
    )
    if not m:
        return None, 0.0
    try:
        valor = datetime.strptime(re.sub(r"[.-]", "/", m.group(1)), "%d/%m/%Y").date()
    except ValueError:
        return m.group(1), 0.2
    return valor.isoformat(), confianza


def _importe(texto: str, rotulos: list[str], confianza: float) -> tuple[str | None, float]:
    for rotulo in rotulos:
        m = re.search(rotulo + r"\s*:?\s*" + _IMPORTE, texto, re.IGNORECASE)
        if m:
            valor = normalizar_importe(m.group(1))
            if valor is not None:
                return valor, confianza
    return None, 0.0


def _iva(texto: str) -> tuple[str | None, float]:
    """Suma las líneas de IVA por alícuota (IVA 21%, IVA 10,5%, ...)."""
    montos = [
        normalizar_importe(m.group(1))
        for m in re.finditer(r"\bIVA\s*\d{1,2}(?:[.,]\d)?\s*%\s*:?\s*" + _IMPORTE, texto, re.IGNORECASE)
    ]
    montos_validos = [Decimal(v) for v in montos if v is not None]
    if montos_validos:
        return f"{sum(montos_validos):.2f}", 0.95
    return _importe(texto, [r"\bI\.?V\.?A\.?(?:\s+Inscripto)?"], 0.7)


def _otros(texto: str) -> tuple[str | None, float]:
    valor, confianza = _importe(texto, [r"(?:Importe\s+)?Otros\s+(?:Tributos|Impuestos)", r"Percepci[oó]n(?:es)?"], 0.9)
    # Sin rótulo de otros tributos se asume cero, con confianza suficiente para no exigir revisión.
    return (valor, confianza) if valor is not None else ("0.00", 0.85)


def _total(texto: str) -> tuple[str | None, float]:
    valor, confianza = _importe(texto, [r"Importe\s+Total"], 0.95)
    if valor is not None:
        return valor, confianza
    return _importe(texto, [r"\bTOTAL"], 0.7)
