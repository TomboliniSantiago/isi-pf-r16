import pytest

from app.cuit import normalizar_cuit
from app.errors import ErrorNegocio


@pytest.mark.parametrize("entrada", ["30-70895432-9", "30708954329", " 30 70895432 9 "])
def test_normaliza_con_o_sin_guiones(entrada):
    assert normalizar_cuit(entrada) == "30-70895432-9"


@pytest.mark.parametrize(
    ("entrada", "mensaje"),
    [
        ("30-70895432-8", "no es válido"),
        ("3070895432", "11 dígitos"),
        ("30-7089543A-9", "11 dígitos"),
        ("", "11 dígitos"),
    ],
)
def test_rechaza_cuit_invalido(entrada, mensaje):
    with pytest.raises(ErrorNegocio, match=mensaje):
        normalizar_cuit(entrada)
