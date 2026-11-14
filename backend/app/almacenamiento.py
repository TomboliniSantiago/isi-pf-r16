"""Almacenamiento del archivo original de los comprobantes digitales (CUU-016).

Los archivos se guardan en la carpeta ALMACENAMIENTO_DIR del servidor (fuera del repositorio), con el hash
SHA-256 del contenido como nombre: el mismo archivo no se duplica y el nombre no depende del usuario.
La base guarda solo la ruta relativa (DOCUMENTO.ruta_archivo).
"""

import hashlib
from pathlib import Path

from app.config import get_settings
from app.errors import ErrorNegocio


def _raiz() -> Path:
    raiz = Path(get_settings().almacenamiento_dir)
    if not raiz.is_absolute():
        raiz = Path(__file__).resolve().parent.parent / raiz  # relativa a backend/
    return raiz


def hash_de(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


def guardar(contenido: bytes, extension: str) -> str:
    """Guarda el archivo y devuelve su ruta relativa (ej. comprobantes/ab/ab12...ef.pdf)."""
    digest = hash_de(contenido)
    relativa = Path("comprobantes") / digest[:2] / f"{digest}.{extension}"
    destino = _raiz() / relativa
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        destino.write_bytes(contenido)
    return relativa.as_posix()


def leer(ruta_relativa: str) -> bytes:
    raiz = _raiz().resolve()
    archivo = (raiz / ruta_relativa).resolve()
    if raiz not in archivo.parents or not archivo.is_file():
        raise ErrorNegocio(404, "No se encontró el archivo original del comprobante.")
    return archivo.read_bytes()
