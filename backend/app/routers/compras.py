from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import Compra, EstadoCompra, Proveedor, Rol, Usuario
from app.schemas_compras import CompraIn, CompraOut, CuentasCompraIn, PropuestaCompraOut, ProveedorCompraOut
from app.schemas_comprobantes import AsientoComprobanteOut, LineaPropuestaOut
from app.services import asientos_service
from app.services import compras_service as servicio

router = APIRouter(prefix="/api/compras", tags=["Compras"])
# Consulta: cualquier usuario con sesión. Registro y anulación: actores de CUU-002.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


def _salidas(db: Session, compras: list[Compra]) -> list[CompraOut]:
    asientos = servicio.asientos_de(db, [c.id_compra for c in compras])
    contras = asientos_service.contra_asientos_de(db, [a.id_asiento for a in asientos.values()])
    proveedores = {c.id_proveedor: db.get(Proveedor, c.id_proveedor) for c in compras}
    salidas = []
    for c in compras:
        proveedor = proveedores.get(c.id_proveedor)
        asiento = asientos.get(c.id_compra)
        contra = contras.get(asiento.id_asiento) if asiento else None
        salidas.append(
            CompraOut(
                id_compra=c.id_compra,
                proveedor=ProveedorCompraOut(
                    id_proveedor=proveedor.id_proveedor,
                    codigo=proveedor.codigo,
                    cuit=proveedor.cuit,
                    razon_social=proveedor.razon_social,
                )
                if proveedor
                else None,
                tipo_comprobante=c.tipo_comprobante,
                punto_venta=c.punto_venta,
                numero_comprobante=c.numero_comprobante,
                numero=c.numero,
                fecha_emision=c.fecha_emision,
                fecha_contable=c.fecha_contable,
                condicion_compra=c.condicion_compra,
                moneda=c.moneda,
                importe_neto_gravado=c.importe_neto_gravado,
                importe_iva=c.importe_iva,
                importe_otros_impuestos=c.importe_otros_impuestos,
                importe_total=c.importe_total,
                estado=c.estado,
                asiento=AsientoComprobanteOut(
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


@router.get("", response_model=list[CompraOut])
def listar(
    desde: date | None = None,
    hasta: date | None = None,
    id_proveedor: int | None = None,
    estado: EstadoCompra | None = None,
    buscar: str | None = None,
    limite: int = Query(500, ge=1, le=2000),
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[CompraOut]:
    return _salidas(db, servicio.listar(db, desde, hasta, id_proveedor, estado, buscar, limite))


@router.post("/propuesta", response_model=PropuestaCompraOut)
def propuesta(datos: CompraIn, _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)) -> PropuestaCompraOut:
    """Pasos 2-6: valida el comprobante, detecta duplicados (2.a) y devuelve el asiento propuesto, sin guardar."""
    p, duplicado = servicio.proponer(db, datos)
    return PropuestaCompraOut(
        lineas=[LineaPropuestaOut(**linea) for linea in p.lineas_out()],
        total_debe=p.total_debe,
        total_haber=p.total_haber,
        diferencia=p.total_debe - p.total_haber,
        balanceado=p.balanceado,
        cuentas_faltantes=p.faltantes,
        duplicado=_salidas(db, [duplicado])[0] if duplicado else None,
    )


@router.get("/{id_compra}", response_model=CompraOut)
def obtener(id_compra: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)) -> CompraOut:
    return _salidas(db, [servicio.obtener(db, id_compra)])[0]


@router.post("", response_model=CompraOut, status_code=201)
def crear(
    datos: CompraIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> CompraOut:
    """CUU-002: registra la compra pendiente o, si datos.confirmar, contabilizada con su asiento."""
    return _salidas(db, [servicio.crear(db, datos, actor, origen_de(request))])[0]


@router.put("/{id_compra}", response_model=CompraOut)
def modificar(
    id_compra: int,
    datos: CompraIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> CompraOut:
    return _salidas(db, [servicio.modificar(db, id_compra, datos, actor, origen_de(request))])[0]


@router.post("/{id_compra}/contabilizar", response_model=CompraOut)
def contabilizar(
    id_compra: int,
    request: Request,
    cuentas: CuentasCompraIn | None = None,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> CompraOut:
    compra = servicio.contabilizar(db, id_compra, cuentas or CuentasCompraIn(), actor, origen_de(request))
    return _salidas(db, [compra])[0]


@router.post("/{id_compra}/anular", response_model=CompraOut)
def anular(
    id_compra: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> CompraOut:
    return _salidas(db, [servicio.anular(db, id_compra, actor, origen_de(request))])[0]
