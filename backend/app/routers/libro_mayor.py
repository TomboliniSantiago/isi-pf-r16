from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import usuario_habilitado
from app.models import Usuario
from app.schemas_libro_mayor import CuentaMayorOut, LibroMayorOut, MovimientoMayorOut
from app.services import libro_mayor_service as servicio

router = APIRouter(prefix="/api/libro-mayor", tags=["Libro Mayor"])
CERO = servicio.CERO


@router.get("", response_model=LibroMayorOut)
def consultar(
    id_cuenta: int,
    desde: date | None = None,
    hasta: date | None = None,
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> LibroMayorOut:
    """CUU-006: movimientos y saldos de una cuenta, o de las cuentas imputables de un rubro, en el período."""
    consultada, mayores = servicio.consultar(db, id_cuenta, desde, hasta)
    cuentas = [
        CuentaMayorOut(
            id_cuenta=m.cuenta.id_cuenta,
            codigo=m.cuenta.codigo,
            nombre=m.cuenta.nombre,
            tipo_cuenta=m.cuenta.tipo_cuenta,
            naturaleza=m.cuenta.naturaleza,
            activa=m.cuenta.esta_activa,
            saldo_inicial=m.saldo_inicial,
            total_debe=m.total_debe,
            total_haber=m.total_haber,
            saldo_final=m.saldo_final,
            movimientos=[
                MovimientoMayorOut(
                    fecha=mov.asiento.fecha,
                    id_asiento=mov.asiento.id_asiento,
                    numero_asiento=mov.asiento.numero_asiento,
                    tipo_origen=mov.asiento.tipo_origen,
                    estado=mov.asiento.estado,
                    concepto=mov.asiento.concepto,
                    referencia=mov.asiento.referencia,
                    id_venta=mov.asiento.id_venta,
                    id_compra=mov.asiento.id_compra,
                    debe=mov.detalle.debe or CERO,
                    haber=mov.detalle.haber or CERO,
                    saldo=mov.saldo,
                )
                for mov in m.movimientos
            ],
        )
        for m in mayores
    ]
    return LibroMayorOut(
        id_cuenta=consultada.id_cuenta,
        codigo=consultada.codigo,
        nombre=consultada.nombre,
        imputable=consultada.es_imputable,
        desde=desde,
        hasta=hasta,
        cuentas=cuentas,
        saldo_inicial=sum((c.saldo_inicial for c in cuentas), CERO),
        total_debe=sum((c.total_debe for c in cuentas), CERO),
        total_haber=sum((c.total_haber for c in cuentas), CERO),
        saldo_final=sum((c.saldo_final for c in cuentas), CERO),
    )
