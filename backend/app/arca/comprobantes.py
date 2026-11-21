"""Consulta de comprobantes en ARCA (CUU-017 pasos 3-4), desacoplada de la lógica contable.

El contrato es el del web service de constatación de comprobantes de ARCA: se envían el CUIT del emisor, el
tipo, el punto de venta, el número, la fecha, el importe total y el CAE, y ARCA informa si el comprobante
existe y con qué datos fue autorizado (incluido el vencimiento del CAE). La comparación con lo registrado y el
estado fiscal resultante los decide el sistema (validaciones_service), no el adaptador.

Todavía no hay credenciales ni ambiente de homologación de ARCA, así que solo existe ArcaSimulado, con
respuestas repetibles. El servicio real será otra clase con el mismo método `consultar`, que lance
ArcaNoDisponible si no hay conexión o vence el tiempo de espera, y ErrorArca si el servicio responde con error.
"""

from dataclasses import dataclass, replace
from datetime import date, timedelta
from decimal import Decimal
from typing import Protocol

# Código de ARCA de cada tipo de comprobante (tabla de tipos de comprobante del web service).
CODIGO_TIPO = {"Factura A": 1, "Factura B": 6, "Factura C": 11}


@dataclass(frozen=True)
class DatosComprobante:
    """Datos fiscales de un comprobante: los que se envían a ARCA y los que ARCA informa."""

    cuit_emisor: str
    tipo_comprobante: str
    punto_venta: int
    numero: int
    fecha_emision: date
    importe_total: Decimal
    cae: str
    cuit_receptor: str | None = None
    # Solo en la respuesta: vencimiento del CAE según ARCA.
    cae_vencimiento: date | None = None


@dataclass(frozen=True)
class RespuestaArca:
    existe: bool
    # Datos con que ARCA autorizó el comprobante (None si no existe).
    comprobante: DatosComprobante | None = None
    observaciones: tuple[str, ...] = ()


class ArcaNoDisponible(Exception):
    """ARCA no respondió: sin conexión o tiempo de espera agotado (3.a)."""


class ErrorArca(Exception):
    """ARCA respondió con un error del servicio (3.a)."""


class ServicioComprobantes(Protocol):
    def consultar(self, consulta: DatosComprobante) -> RespuestaArca: ...


# CAE de prueba del simulador: cada uno reproduce un camino del caso de uso.
CAE_SIN_RESPUESTA = "99999999999900"  # 3.a: ARCA no responde
CAE_INEXISTENTE = "99999999999901"  # 4.a: el comprobante no existe
CAE_VENCIDO = "99999999999902"  # 5.a: el CAE venció antes de la fecha de emisión
CAE_TOTAL_DISTINTO = "99999999999903"  # 6.a: ARCA informa otro importe total
CAE_ERROR_SERVICIO = "99999999999904"  # 3.a: ARCA responde con error
DIAS_VIGENCIA_CAE = 10


class ArcaSimulado:
    """Respuestas repetibles para desarrollo y demostraciones. Con los CAE de prueba se reproduce cada camino
    alternativo; con cualquier otro CAE, ARCA informa el comprobante tal como se envió, con el CAE vigente
    (vence 10 días después de la emisión)."""

    def consultar(self, consulta: DatosComprobante) -> RespuestaArca:
        if consulta.cae == CAE_SIN_RESPUESTA:
            raise ArcaNoDisponible("Tiempo de espera agotado (simulado).")
        if consulta.cae == CAE_ERROR_SERVICIO:
            raise ErrorArca("Error interno del servicio de ARCA (simulado).")
        if consulta.cae == CAE_INEXISTENTE:
            return RespuestaArca(existe=False, observaciones=("No existe un comprobante con los datos informados.",))
        vencimiento = consulta.fecha_emision + timedelta(days=DIAS_VIGENCIA_CAE)
        if consulta.cae == CAE_VENCIDO:
            vencimiento = consulta.fecha_emision - timedelta(days=1)
        total = consulta.importe_total
        if consulta.cae == CAE_TOTAL_DISTINTO:
            total += Decimal("100.00")
        return RespuestaArca(
            existe=True, comprobante=replace(consulta, importe_total=total, cae_vencimiento=vencimiento)
        )


def get_servicio_comprobantes() -> ServicioComprobantes:
    return ArcaSimulado()
