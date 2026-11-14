"""Adaptador de OCR: obtiene el texto de un comprobante PDF o imagen, desacoplado de la lógica contable.

- PDF con texto (las facturas electrónicas de ARCA lo son): se lee el texto con pypdf (confianza 1).
- Imagen (PNG/JPG) o PDF escaneado sin texto: se reconoce con Tesseract y la confianza es el promedio de
  la que informa Tesseract por palabra. Si Tesseract no está instalado, se devuelve un texto vacío con un
  aviso: el usuario completa los campos a mano (CUU-016 3.a).

Para sumar otro motor (por ejemplo, Google Vision) alcanza con otra implementación de `MotorOcr`.
"""

import io
import logging
from dataclasses import dataclass
from enum import StrEnum
from functools import lru_cache
from typing import Protocol

from app.config import get_settings
from app.errors import ErrorNegocio

log = logging.getLogger(__name__)


class Formato(StrEnum):
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"


TIPO_CONTENIDO = {Formato.PDF: "application/pdf", Formato.PNG: "image/png", Formato.JPG: "image/jpeg"}


@dataclass
class TextoOcr:
    texto: str
    # Confianza del reconocimiento (0 a 1); None si no se pudo reconocer nada.
    confianza: float | None
    motor: str
    aviso: str | None = None


class MotorOcr(Protocol):
    def leer(self, contenido: bytes, formato: Formato) -> TextoOcr: ...


def detectar_formato(contenido: bytes) -> Formato:
    """2.a: el formato se determina por el contenido (no por la extensión del nombre)."""
    if contenido.startswith(b"%PDF-"):
        return Formato.PDF
    if contenido.startswith(b"\x89PNG\r\n\x1a\n"):
        return Formato.PNG
    if contenido.startswith(b"\xff\xd8\xff"):
        return Formato.JPG
    raise ErrorNegocio(422, "El formato del archivo no es válido: se admiten comprobantes en PDF, PNG o JPG.")


class MotorPdfTesseract:
    """pypdf para el texto de los PDF y Tesseract para imágenes y PDF escaneados."""

    def leer(self, contenido: bytes, formato: Formato) -> TextoOcr:
        if formato == Formato.PDF:
            return self._leer_pdf(contenido)
        return self._reconocer_imagenes([contenido])

    def _leer_pdf(self, contenido: bytes) -> TextoOcr:
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError

        try:
            lector = PdfReader(io.BytesIO(contenido))
            paginas = list(lector.pages)
            texto = "\n".join(pagina.extract_text() or "" for pagina in paginas)
        except (PdfReadError, ValueError, KeyError) as exc:
            raise ErrorNegocio(422, "No se pudo leer el PDF: el archivo está dañado o protegido.") from exc
        if texto.strip():
            return TextoOcr(texto=texto, confianza=1.0, motor="pdf-texto")
        # PDF escaneado: se reconocen las imágenes de sus páginas.
        imagenes = [imagen.data for pagina in paginas for imagen in pagina.images]
        if not imagenes:
            return TextoOcr(texto="", confianza=None, motor="pdf-texto", aviso="El PDF no contiene texto ni imágenes.")
        return self._reconocer_imagenes(imagenes)

    def _reconocer_imagenes(self, imagenes: list[bytes]) -> TextoOcr:
        import pytesseract
        from PIL import Image, UnidentifiedImageError

        configuracion = get_settings()
        if configuracion.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = configuracion.tesseract_cmd
        textos: list[str] = []
        confianzas: list[float] = []
        try:
            idioma = _idioma_tesseract()
            for datos in imagenes:
                with Image.open(io.BytesIO(datos)) as imagen:
                    resultado = pytesseract.image_to_data(imagen, lang=idioma, output_type=pytesseract.Output.DICT)
                textos.append(_texto_por_lineas(resultado))
                confianzas.extend(
                    float(c) / 100
                    for c, p in zip(resultado["conf"], resultado["text"], strict=True)
                    if p.strip() and float(c) >= 0
                )
        except pytesseract.TesseractNotFoundError:
            return TextoOcr(
                texto="",
                confianza=None,
                motor="ninguno",
                aviso="El reconocimiento de imágenes no está disponible en el servidor (Tesseract no está "
                "instalado): complete los datos del comprobante a mano.",
            )
        except UnidentifiedImageError as exc:
            raise ErrorNegocio(422, "No se pudo leer la imagen: el archivo está dañado.") from exc
        texto = "\n".join(textos)
        confianza = sum(confianzas) / len(confianzas) if confianzas else None
        aviso = None if texto.strip() else "No se reconoció texto en la imagen."
        return TextoOcr(texto=texto, confianza=confianza, motor="tesseract", aviso=aviso)


def _texto_por_lineas(resultado: dict) -> str:
    """Rearma el texto de Tesseract respetando bloques y líneas."""
    lineas: dict[tuple[int, int, int], list[str]] = {}
    for i, palabra in enumerate(resultado["text"]):
        if palabra.strip():
            clave = (resultado["block_num"][i], resultado["par_num"][i], resultado["line_num"][i])
            lineas.setdefault(clave, []).append(palabra)
    return "\n".join(" ".join(palabras) for _, palabras in sorted(lineas.items()))


@lru_cache
def _idioma_tesseract() -> str:
    import pytesseract

    try:
        return "spa" if "spa" in pytesseract.get_languages(config="") else "eng"
    except pytesseract.TesseractError:  # versiones antiguas sin --list-langs
        return "eng"


def get_motor() -> MotorOcr:
    """Dependencia de FastAPI: las pruebas la reemplazan por un motor simulado."""
    return MotorPdfTesseract()
