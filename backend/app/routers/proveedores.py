from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.arca.padron import Padron, get_padron
from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import CondicionIva, Rol, Usuario
from app.schemas_proveedores import (
    ComprobanteOut,
    ConsultaCuitOut,
    DatosPadronOut,
    ProveedorDetalleOut,
    ProveedorIn,
    ProveedorOut,
    ProveedorResumen,
    ValidacionOut,
)
from app.services import proveedores_service as servicio

router = APIRouter(prefix="/api/proveedores", tags=["Proveedores"])
# Consulta: cualquier usuario con sesión. Modificación: los actores de CUU-008.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


@router.get("", response_model=list[ProveedorOut])
def listar(
    buscar: str | None = Query(None, max_length=100, description="Razón social o CUIT (con o sin guiones)"),
    condicion_iva: CondicionIva | None = None,
    activo: bool | None = None,
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[ProveedorOut]:
    return [ProveedorOut.de(p) for p in servicio.listar(db, buscar, condicion_iva, activo)]


@router.get("/consulta-cuit", response_model=ConsultaCuitOut)
def consultar_cuit(
    cuit: str = Query(..., max_length=20),
    _: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
    padron: Padron = Depends(get_padron),
) -> ConsultaCuitOut:
    """Pasos 3-4: consulta el padrón de ARCA y si ya hay un proveedor con ese CUIT."""
    cuit, datos, existente = servicio.consultar_cuit(db, cuit, padron)
    return ConsultaCuitOut(
        cuit=cuit,
        en_padron=datos is not None,
        datos=DatosPadronOut(
            razon_social=datos.razon_social,
            condicion_iva=datos.condicion_iva,
            domicilio=datos.domicilio,
            localidad=datos.localidad,
            provincia=datos.provincia,
        )
        if datos
        else None,
        proveedor_existente=ProveedorResumen(
            id_proveedor=existente.id_proveedor,
            codigo=existente.codigo,
            cuit=existente.cuit,
            razon_social=existente.razon_social,
            activo=existente.esta_activo,
        )
        if existente
        else None,
    )


@router.get("/{id_proveedor}", response_model=ProveedorDetalleOut)
def obtener(
    id_proveedor: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> ProveedorDetalleOut:
    proveedor = servicio.obtener(db, id_proveedor)
    compras = servicio.comprobantes(db, id_proveedor)
    return ProveedorDetalleOut(
        **ProveedorOut.de(proveedor).model_dump(),
        cantidad_comprobantes=len(compras),
        comprobantes_pendientes=sum(servicio.es_pendiente(c, asentada) for c, asentada in compras),
    )


@router.get("/{id_proveedor}/comprobantes", response_model=list[ComprobanteOut])
def comprobantes(
    id_proveedor: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> list[ComprobanteOut]:
    """2.c.2: historial de comprobantes asociados al proveedor."""
    servicio.obtener(db, id_proveedor)
    return [
        ComprobanteOut(
            id_compra=c.id_compra,
            tipo_comprobante=c.tipo_comprobante,
            numero=c.numero,
            fecha_emision=c.fecha_emision,
            moneda=c.moneda,
            importe_total=c.importe_total,
            asentado=asentada,
            pendiente=servicio.es_pendiente(c, asentada),
        )
        for c, asentada in servicio.comprobantes(db, id_proveedor)
    ]


@router.post("", response_model=ProveedorOut, status_code=201)
def crear(
    datos: ProveedorIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ProveedorOut:
    return ProveedorOut.de(servicio.crear(db, datos, actor, origen_de(request)))


@router.put("/{id_proveedor}", response_model=ProveedorOut)
def modificar(
    id_proveedor: int,
    datos: ProveedorIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> ProveedorOut:
    return ProveedorOut.de(servicio.modificar(db, id_proveedor, datos, actor, origen_de(request)))


@router.get("/{id_proveedor}/verificar-baja", response_model=ValidacionOut)
def verificar_baja(
    id_proveedor: int, _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ValidacionOut:
    """2.b.2: informa si el proveedor puede darse de baja, antes de pedir la confirmación."""
    servicio.verificar_baja(db, id_proveedor)
    return ValidacionOut(valido=True, mensaje="El proveedor no tiene comprobantes pendientes de procesamiento.")


@router.post("/{id_proveedor}/baja", response_model=ProveedorOut)
def dar_de_baja(
    id_proveedor: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ProveedorOut:
    return ProveedorOut.de(servicio.dar_de_baja(db, id_proveedor, actor, origen_de(request)))


@router.post("/{id_proveedor}/reactivar", response_model=ProveedorOut)
def reactivar(
    id_proveedor: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ProveedorOut:
    return ProveedorOut.de(servicio.reactivar(db, id_proveedor, actor, origen_de(request)))
