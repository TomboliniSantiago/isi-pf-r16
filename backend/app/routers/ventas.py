from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import Cliente, EstadoVenta, Rol, Usuario, Venta
from app.schemas_ventas import (
    AsientoVentaOut,
    ClienteVentaOut,
    CuentasVentaIn,
    LineaPropuestaOut,
    PropuestaOut,
    VentaIn,
    VentaOut,
)
from app.services import asientos_service
from app.services import ventas_service as servicio

router = APIRouter(prefix="/api/ventas", tags=["Ventas"])
# Consulta: cualquier usuario con sesión. Registro y anulación: actores de CUU-001.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


def _salidas(db: Session, ventas: list[Venta]) -> list[VentaOut]:
    ids = [v.id_venta for v in ventas]
    asientos = servicio.asientos_de(db, ids)
    contras = asientos_service.contra_asientos_de(db, [a.id_asiento for a in asientos.values()])
    clientes = {v.id_cliente: db.get(Cliente, v.id_cliente) for v in ventas}
    salidas = []
    for v in ventas:
        cliente = clientes.get(v.id_cliente)
        asiento = asientos.get(v.id_venta)
        contra = contras.get(asiento.id_asiento) if asiento else None
        salidas.append(
            VentaOut(
                id_venta=v.id_venta,
                cliente=ClienteVentaOut(
                    id_cliente=cliente.id_cliente,
                    codigo=cliente.codigo,
                    cuit=cliente.cuit,
                    razon_social=cliente.razon_social,
                )
                if cliente
                else None,
                tipo_comprobante=v.tipo_comprobante,
                punto_venta=v.punto_venta,
                numero_comprobante=v.numero_comprobante,
                numero=v.numero,
                fecha_emision=v.fecha_emision,
                fecha_contable=v.fecha_contable,
                condicion_venta=v.condicion_venta,
                moneda=v.moneda,
                importe_neto_gravado=v.importe_neto_gravado,
                importe_iva=v.importe_iva,
                importe_otros_impuestos=v.importe_otros_impuestos,
                importe_total=v.importe_total,
                cae=v.cae,
                estado=v.estado,
                asiento=AsientoVentaOut(
                    id_asiento=asiento.id_asiento,
                    numero_asiento=asiento.numero_asiento,
                    estado=asiento.estado,
                    revertido_por=contra.numero_asiento if contra else None,
                )
                if asiento
                else None,
            )
        )
    return salidas


@router.get("", response_model=list[VentaOut])
def listar(
    desde: date | None = None,
    hasta: date | None = None,
    id_cliente: int | None = None,
    estado: EstadoVenta | None = None,
    buscar: str | None = None,
    limite: int = Query(500, ge=1, le=2000),
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[VentaOut]:
    return _salidas(db, servicio.listar(db, desde, hasta, id_cliente, estado, buscar, limite))


@router.post("/propuesta", response_model=PropuestaOut)
def propuesta(datos: VentaIn, _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)) -> PropuestaOut:
    """Pasos 2-6: valida el comprobante, detecta duplicados (2.a) y devuelve el asiento propuesto, sin guardar."""
    p, duplicado = servicio.proponer(db, datos)
    return PropuestaOut(
        lineas=[
            LineaPropuestaOut(
                rol=linea.rol,
                descripcion=linea.descripcion,
                id_cuenta=linea.cuenta.id_cuenta if linea.cuenta else None,
                codigo=linea.cuenta.codigo if linea.cuenta else None,
                nombre=linea.cuenta.nombre if linea.cuenta else None,
                debe=linea.debe,
                haber=linea.haber,
            )
            for linea in p.lineas
        ],
        total_debe=p.total_debe,
        total_haber=p.total_haber,
        diferencia=p.total_debe - p.total_haber,
        balanceado=p.balanceado,
        cuentas_faltantes=p.faltantes,
        duplicado=_salidas(db, [duplicado])[0] if duplicado else None,
    )


@router.get("/{id_venta}", response_model=VentaOut)
def obtener(id_venta: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)) -> VentaOut:
    return _salidas(db, [servicio.obtener(db, id_venta)])[0]


@router.post("", response_model=VentaOut, status_code=201)
def crear(
    datos: VentaIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> VentaOut:
    """CUU-001: registra la venta pendiente o, si datos.confirmar, contabilizada con su asiento."""
    return _salidas(db, [servicio.crear(db, datos, actor, origen_de(request))])[0]


@router.put("/{id_venta}", response_model=VentaOut)
def modificar(
    id_venta: int,
    datos: VentaIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> VentaOut:
    return _salidas(db, [servicio.modificar(db, id_venta, datos, actor, origen_de(request))])[0]


@router.post("/{id_venta}/contabilizar", response_model=VentaOut)
def contabilizar(
    id_venta: int,
    request: Request,
    cuentas: CuentasVentaIn | None = None,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> VentaOut:
    venta = servicio.contabilizar(db, id_venta, cuentas or CuentasVentaIn(), actor, origen_de(request))
    return _salidas(db, [venta])[0]


@router.post("/{id_venta}/anular", response_model=VentaOut)
def anular(
    id_venta: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> VentaOut:
    return _salidas(db, [servicio.anular(db, id_venta, actor, origen_de(request))])[0]
