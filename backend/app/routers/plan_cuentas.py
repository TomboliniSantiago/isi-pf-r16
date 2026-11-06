from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import origen_de, requiere_roles, usuario_habilitado
from app.models import ClavePredeterminada, PlanCuenta, Rol, TipoCuenta, Usuario
from app.schemas_plan_cuentas import (
    CuentaDetalleOut,
    CuentaIn,
    CuentaOut,
    CuentaResumen,
    MovimientoOut,
    PredeterminadaIn,
    PredeterminadaOut,
    ValidacionOut,
)
from app.services import plan_cuentas_service as servicio

router = APIRouter(prefix="/api/plan-cuentas", tags=["Plan de Cuentas"])
# Consulta: cualquier usuario con sesión. Modificación: Contador y Administrador.
puede_editar = requiere_roles(Rol.CONTADOR, Rol.ADMINISTRADOR)


def _resumen(cuenta: PlanCuenta | None) -> CuentaResumen | None:
    return CuentaResumen(id_cuenta=cuenta.id_cuenta, codigo=cuenta.codigo, nombre=cuenta.nombre) if cuenta else None


def _predeterminada(clave: ClavePredeterminada, cuenta: PlanCuenta | None) -> PredeterminadaOut:
    regla = servicio.REGLAS_PREDETERMINADA[clave]
    return PredeterminadaOut(
        clave=clave,
        descripcion=servicio.DESCRIPCION_PREDETERMINADA[clave],
        cuenta=_resumen(cuenta),
        tipos_admitidos=list(regla.tipos),
        naturaleza=regla.naturaleza,
        requisito=servicio.describir_regla(clave),
    )


def _salida(db: Session, cuenta: PlanCuenta) -> CuentaOut:
    padre = db.get(PlanCuenta, cuenta.id_cuenta_padre) if cuenta.id_cuenta_padre else None
    return CuentaOut.de(cuenta, padre.codigo if padre else None)


@router.get("", response_model=list[CuentaOut])
def listar(
    buscar: str | None = Query(None, max_length=100),
    tipo: TipoCuenta | None = None,
    activa: bool | None = None,
    imputable: bool | None = None,
    _: Usuario = Depends(usuario_habilitado),
    db: Session = Depends(get_db),
) -> list[CuentaOut]:
    return [CuentaOut.de(c, padre) for c, padre in servicio.listar(db, buscar, tipo, activa, imputable)]


@router.get("/predeterminadas", response_model=list[PredeterminadaOut])
def listar_predeterminadas(
    _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> list[PredeterminadaOut]:
    return [_predeterminada(clave, cuenta) for clave, cuenta in servicio.listar_predeterminadas(db)]


@router.put("/predeterminadas/{clave}", response_model=PredeterminadaOut)
def asignar_predeterminada(
    clave: ClavePredeterminada,
    datos: PredeterminadaIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> PredeterminadaOut:
    cuenta = servicio.asignar_predeterminada(db, clave, datos.id_cuenta, actor, origen_de(request))
    return _predeterminada(clave, cuenta)


@router.post("/validar", response_model=ValidacionOut)
def validar(
    datos: CuentaIn,
    id_cuenta: int | None = Query(None, description="Cuenta que se modifica; vacío para un alta"),
    _: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> ValidacionOut:
    """Paso 5 / 2.a.4: valida los datos sin guardarlos, para mostrarlos antes de confirmar."""
    servicio.validar(db, datos, id_cuenta)
    return ValidacionOut(valido=True, mensaje="Los datos son válidos y mantienen la consistencia del Plan de Cuentas.")


@router.get("/{id_cuenta}", response_model=CuentaDetalleOut)
def obtener(
    id_cuenta: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> CuentaDetalleOut:
    cuenta = servicio.obtener(db, id_cuenta)
    return CuentaDetalleOut(
        **_salida(db, cuenta).model_dump(),
        ruta=[_resumen(c) for c in servicio.ruta(db, cuenta)],
        cantidad_hijas=servicio.cantidad_hijas(db, id_cuenta),
        cantidad_movimientos=servicio.cantidad_movimientos(db, id_cuenta),
        predeterminada_para=servicio.predeterminada_para(db, id_cuenta),
    )


@router.get("/{id_cuenta}/movimientos", response_model=list[MovimientoOut])
def movimientos(
    id_cuenta: int, _: Usuario = Depends(usuario_habilitado), db: Session = Depends(get_db)
) -> list[MovimientoOut]:
    return [
        MovimientoOut(
            id_asiento=asiento.id_asiento,
            numero_asiento=asiento.numero_asiento,
            fecha=asiento.fecha,
            concepto=asiento.concepto,
            estado=asiento.estado,
            debe=detalle.debe or 0,
            haber=detalle.haber or 0,
        )
        for detalle, asiento in servicio.movimientos(db, id_cuenta)
    ]


@router.post("", response_model=CuentaOut, status_code=201)
def crear(
    datos: CuentaIn, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> CuentaOut:
    return _salida(db, servicio.crear(db, datos, actor, origen_de(request)))


@router.put("/{id_cuenta}", response_model=CuentaOut)
def modificar(
    id_cuenta: int,
    datos: CuentaIn,
    request: Request,
    actor: Usuario = Depends(puede_editar),
    db: Session = Depends(get_db),
) -> CuentaOut:
    return _salida(db, servicio.modificar(db, id_cuenta, datos, actor, origen_de(request)))


@router.get("/{id_cuenta}/verificar-baja", response_model=ValidacionOut)
def verificar_baja(id_cuenta: int, _: Usuario = Depends(puede_editar), db: Session = Depends(get_db)) -> ValidacionOut:
    """2.b.1-2.b.2: informa si la cuenta puede darse de baja, antes de pedir la confirmación."""
    servicio.verificar_baja(db, id_cuenta)
    return ValidacionOut(valido=True, mensaje="La cuenta no tiene movimientos ni cuentas dependientes activas.")


@router.post("/{id_cuenta}/baja", response_model=CuentaOut)
def dar_de_baja(
    id_cuenta: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> CuentaOut:
    return _salida(db, servicio.dar_de_baja(db, id_cuenta, actor, origen_de(request)))


@router.post("/{id_cuenta}/reactivar", response_model=CuentaOut)
def reactivar(
    id_cuenta: int, request: Request, actor: Usuario = Depends(puede_editar), db: Session = Depends(get_db)
) -> CuentaOut:
    return _salida(db, servicio.reactivar(db, id_cuenta, actor, origen_de(request)))
