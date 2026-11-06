"""Consulta al padrón de ARCA (CUU-007 paso 3), desacoplada de la lógica de clientes.

Todavía no hay credenciales ni ambiente de homologación de ARCA, así que por ahora solo existe
PadronSimulado, con respuestas repetibles para un conjunto fijo de CUIT. El servicio real (web service
de padrón de ARCA) se implementará como otra clase con el mismo método `consultar`.
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DatosPadron:
    cuit: str
    razon_social: str
    condicion_iva: str
    domicilio: str
    localidad: str
    provincia: str


class Padron(Protocol):
    def consultar(self, cuit: str) -> DatosPadron | None:
        """Datos del contribuyente, o None si el CUIT no figura en el padrón."""
        ...


_SIMULADOS = [
    # Contribuyentes que no están en los datos de prueba: sirven para probar el autocompletado.
    DatosPadron(
        "30-71589631-8",
        "Electrónica del Centro S.A.",
        "Responsable Inscripto",
        "Av. Aristóbulo del Valle 5600",
        "Santa Fe",
        "Santa Fe",
    ),
    DatosPadron(
        "30-70777888-8",
        "Servicios Informáticos Paraná S.R.L.",
        "Responsable Inscripto",
        "Urquiza 1450",
        "Paraná",
        "Entre Ríos",
    ),
    DatosPadron("20-31456789-8", "Pablo Rodríguez", "Monotributo", "Córdoba 2210", "Rosario", "Santa Fe"),
    DatosPadron("27-40123456-5", "Valeria Sosa", "Consumidor Final", "Lavalle 3150", "Santa Fe", "Santa Fe"),
    DatosPadron("33-71234567-0", "Cooperativa Escolar Alem", "Exento", "Alem 980", "Esperanza", "Santa Fe"),
    # Clientes de los datos de prueba: el padrón los encuentra y el sistema detecta el duplicado.
    DatosPadron(
        "30-70895432-9",
        "Comercial Santa Fe S.A.",
        "Responsable Inscripto",
        "Bv. Pellegrini 2450",
        "Santa Fe",
        "Santa Fe",
    ),
    DatosPadron(
        "30-71234099-8", "Tecnored Córdoba S.R.L.", "Responsable Inscripto", "Av. Colón 1234", "Córdoba", "Córdoba"
    ),
    # Proveedores que no están en los datos de prueba.
    DatosPadron(
        "30-71045678-6",
        "Insumos Gráficos del Sur S.A.",
        "Responsable Inscripto",
        "Av. Peñaloza 7400",
        "Santa Fe",
        "Santa Fe",
    ),
    DatosPadron(
        "30-70654321-6", "Logística Litoral S.R.L.", "Responsable Inscripto", "Ruta 11 Km 455", "Recreo", "Santa Fe"
    ),
    DatosPadron("20-25789456-9", "Jorge Benítez", "Monotributo", "Salta 2780", "Santa Fe", "Santa Fe"),
    # Proveedor de los datos de prueba: el sistema detecta el duplicado.
    DatosPadron(
        "30-70123456-8",
        "Mayorista Informático del Litoral S.A.",
        "Responsable Inscripto",
        "Ruta 168 Km 3",
        "Santa Fe",
        "Santa Fe",
    ),
]


class PadronSimulado:
    """Respuestas fijas para desarrollo y demostraciones. Un CUIT que no está en la lista no figura."""

    def __init__(self, contribuyentes: list[DatosPadron] | None = None):
        self._por_cuit = {d.cuit: d for d in (contribuyentes if contribuyentes is not None else _SIMULADOS)}

    def consultar(self, cuit: str) -> DatosPadron | None:
        return self._por_cuit.get(cuit)


def get_padron() -> Padron:
    return PadronSimulado()
