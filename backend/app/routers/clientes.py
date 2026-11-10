from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.arca.padron import Padron, get_padron
from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import CondicionIva, Rol, Usuario
from app.schemas_clientes import (
    ClienteDetalleOut,
    ClienteIn,
    ClienteOut,
    ClienteResumen,
    ComprobanteOut,
    ConsultaCuitOut,
    DatosPadronOut,
    ValidacionOut,
)
from app.services import clientes_service as servicio

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])
# Consulta: cualquier usuario con sesión. Modificación: los actores de CUU-007.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


@router.get("", response_model=list[ClienteOut])
def listar(
    buscar: str | None = Query(None, max_length=100, description="Razón social o CUIT (con o sin guiones)"),
    condicion_iva: CondicionIva | None = None,
    activo: bool | None = None,
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[ClienteOut]:
    return [ClienteOut.de(c) for c in servicio.listar(db, buscar, condicion_iva, activo)]


@router.get("/consulta-cuit", response_model=ConsultaCuitOut)
def consultar_cuit(
    cuit: str = Query(..., max_length=20),
    _: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
    padron: Padron = Depends(get_padron),
) -> ConsultaCuitOut:
    """Pasos 3-4: consulta el padrón de ARCA y si ya hay un cliente con ese CUIT."""
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
        cliente_existente=ClienteResumen(
            id_cliente=existente.id_cliente,
            codigo=existente.codigo,
            cuit=existente.cuit,
            razon_social=existente.razon_social,
            activo=existente.esta_activo,
        )
        if existente
        else None,
    )


@router.get("/{id_cliente}", response_model=ClienteDetalleOut)
def obtener(
    id_cliente: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> ClienteDetalleOut:
    cliente = servicio.obtener(db, id_cliente)
    ventas = servicio.comprobantes(db, id_cliente)
    return ClienteDetalleOut(
        **ClienteOut.de(cliente).model_dump(),
        cantidad_comprobantes=len(ventas),
        comprobantes_pendientes=sum(servicio.es_pendiente(v, asentada) for v, asentada in ventas),
    )


@router.get("/{id_cliente}/comprobantes", response_model=list[ComprobanteOut])
def comprobantes(
    id_cliente: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> list[ComprobanteOut]:
    """2.b.2: historial de comprobantes asociados al cliente."""
    servicio.obtener(db, id_cliente)
    return [
        ComprobanteOut(
            id_venta=v.id_venta,
            tipo_comprobante=v.tipo_comprobante,
            numero=v.numero,
            fecha_emision=v.fecha_emision,
            moneda=v.moneda,
            importe_total=v.importe_total,
            cae=v.cae,
            asentado=asentada,
            pendiente=servicio.es_pendiente(v, asentada),
        )
        for v, asentada in servicio.comprobantes(db, id_cliente)
    ]


@router.post("", response_model=ClienteOut, status_code=201)
def crear(
    datos: ClienteIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ClienteOut:
    return ClienteOut.de(servicio.crear(db, datos, actor, origen_de(request)))


@router.put("/{id_cliente}", response_model=ClienteOut)
def modificar(
    id_cliente: int,
    datos: ClienteIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> ClienteOut:
    return ClienteOut.de(servicio.modificar(db, id_cliente, datos, actor, origen_de(request)))


@router.get("/{id_cliente}/verificar-baja", response_model=ValidacionOut)
def verificar_baja(id_cliente: int, _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)) -> ValidacionOut:
    """2.c.2: informa si el cliente puede darse de baja, antes de pedir la confirmación."""
    servicio.verificar_baja(db, id_cliente)
    return ValidacionOut(valido=True, mensaje="El cliente no tiene comprobantes pendientes de procesamiento.")


@router.post("/{id_cliente}/baja", response_model=ClienteOut)
def dar_de_baja(
    id_cliente: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ClienteOut:
    return ClienteOut.de(servicio.dar_de_baja(db, id_cliente, actor, origen_de(request)))


@router.post("/{id_cliente}/reactivar", response_model=ClienteOut)
def reactivar(
    id_cliente: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> ClienteOut:
    return ClienteOut.de(servicio.reactivar(db, id_cliente, actor, origen_de(request)))
