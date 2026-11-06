"""CUIT/CUIL: normalización y dígito verificador (algoritmo módulo 11 de ARCA)."""

import re

from app.errors import ErrorNegocio

_PESOS = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)


def digito_verificador(base: str) -> int | None:
    """Dígito verificador para los 10 primeros dígitos; None si la combinación no es válida."""
    resto = 11 - sum(int(d) * p for d, p in zip(base, _PESOS, strict=True)) % 11
    if resto == 11:
        return 0
    return None if resto == 10 else resto


def normalizar_cuit(texto: str) -> str:
    """Acepta el CUIT con o sin guiones y lo devuelve como XX-XXXXXXXX-X. Lanza 422 si no es válido."""
    digitos = re.sub(r"[\s-]", "", texto or "")
    if not re.fullmatch(r"\d{11}", digitos):
        raise ErrorNegocio(422, "El CUIT debe tener 11 dígitos, por ejemplo 30-71234567-8.")
    if digito_verificador(digitos[:10]) != int(digitos[10]):
        raise ErrorNegocio(
            422, f"El CUIT {digitos[:2]}-{digitos[2:10]}-{digitos[10]} no es válido: revise los dígitos."
        )
    return f"{digitos[:2]}-{digitos[2:10]}-{digitos[10]}"
