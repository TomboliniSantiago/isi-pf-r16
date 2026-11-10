from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import AsientoContable, EstadoAsiento, OrigenAsiento, Rol, Usuario
from app.schemas_asientos import AsientoIn, AsientoOut, LineaIn, LineaOut, TotalesOut
from app.services import asientos_service as servicio

router = APIRouter(prefix="/api/asientos", tags=["Libro Diario"])
# Consulta: cualquier usuario con sesión. Registro, modificación y anulación: actores de CUU-003/004.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRATIVO)


def _salidas(db: Session, asientos: list[AsientoContable]) -> list[AsientoOut]:
    ids = [a.id_asiento for a in asientos]
    lineas = servicio.lineas_de(db, ids)
    contras = servicio.contra_asientos_de(db, ids)
    revertidos = {
        a.id_asiento_revertido: db.get(AsientoContable, a.id_asiento_revertido)
        for a in asientos
        if a.id_asiento_revertido is not None
    }
    salidas = []
    for a in asientos:
        detalle = [
            LineaOut(
                id_detalle_asiento=d.id_detalle_asiento,
                id_cuenta=d.id_cuenta,
                codigo=c.codigo,
                nombre=c.nombre,
                debe=d.debe or servicio.CERO,
                haber=d.haber or servicio.CERO,
            )
            for d, c in lineas[a.id_asiento]
        ]
        revertido = revertidos.get(a.id_asiento_revertido) if a.id_asiento_revertido else None
        contra = contras.get(a.id_asiento)
        salidas.append(
            AsientoOut(
                id_asiento=a.id_asiento,
                numero_asiento=a.numero_asiento,
                fecha=a.fecha,
                concepto=a.concepto,
                referencia=a.referencia,
                tipo_origen=a.tipo_origen,
                estado=a.estado,
                id_venta=a.id_venta,
                id_compra=a.id_compra,
                revierte_a=revertido.numero_asiento if revertido else None,
                revertido_por=contra.numero_asiento if contra else None,
                total_debe=sum((linea.debe for linea in detalle), servicio.CERO),
                total_haber=sum((linea.haber for linea in detalle), servicio.CERO),
                lineas=detalle,
            )
        )
    return salidas


@router.get("", response_model=list[AsientoOut])
def listar(
    desde: date | None = None,
    hasta: date | None = None,
    id_cuenta: int | None = None,
    tipo_origen: OrigenAsiento | None = None,
    estado: EstadoAsiento | None = None,
    limite: int = Query(500, ge=1, le=2000),
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[AsientoOut]:
    """CUU-003 pasos 1-2: asientos del Libro Diario con su detalle, según los filtros."""
    return _salidas(db, servicio.listar(db, desde, hasta, id_cuenta, tipo_origen, estado, limite))


@router.post("/totales", response_model=TotalesOut)
def totales(lineas: list[LineaIn], _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)) -> TotalesOut:
    """CUU-004 pasos 2-3: valida cuentas e importes y devuelve los totales y la diferencia, sin guardar."""
    t = servicio.validar_lineas(db, lineas)
    return TotalesOut(total_debe=t.debe, total_haber=t.haber, diferencia=t.diferencia, balanceado=t.balanceado)


@router.get("/{id_asiento}", response_model=AsientoOut)
def obtener(id_asiento: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)) -> AsientoOut:
    """CUU-003 paso 3: asiento completo."""
    return _salidas(db, [servicio.obtener(db, id_asiento)])[0]


@router.post("", response_model=AsientoOut, status_code=201)
def crear(
    datos: AsientoIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> AsientoOut:
    """CUU-004: registra un asiento manual como borrador o contabilizado (datos.confirmar)."""
    return _salidas(db, [servicio.crear(db, datos, actor, origen_de(request))])[0]


@router.post("/{id_asiento}/confirmar", response_model=AsientoOut)
def confirmar(
    id_asiento: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> AsientoOut:
    return _salidas(db, [servicio.confirmar(db, id_asiento, actor, origen_de(request))])[0]


@router.put("/{id_asiento}", response_model=AsientoOut)
def modificar(
    id_asiento: int,
    datos: AsientoIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> AsientoOut:
    """CUU-003 3.a: anula el asiento (contra-asiento si estaba asentado) y devuelve el asiento nuevo."""
    return _salidas(db, [servicio.modificar(db, id_asiento, datos, actor, origen_de(request))])[0]


@router.post("/{id_asiento}/anular", response_model=AsientoOut)
def anular(
    id_asiento: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> AsientoOut:
    """CUU-003 3.b: devuelve el contra-asiento generado, o el borrador descartado."""
    return _salidas(db, [servicio.anular(db, id_asiento, actor, origen_de(request))])[0]
