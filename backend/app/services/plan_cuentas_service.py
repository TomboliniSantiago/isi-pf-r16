"""CUU-005 Gestionar Plan de Cuentas (alta, modificación, baja lógica y consulta).

Consistencia de la estructura (pasos 4, 4.a, 4.b y 2.a.2-2.a.3):
- Código: segmentos numéricos separados por punto (ej. 1.1.1.01), único entre todas las cuentas,
  activas o dadas de baja.
- Cuenta sin padre: código de un solo segmento (rubro principal: 1 Activo, 2 Pasivo, ...).
- Cuenta con padre: el padre existe, está activo y no es imputable; el código empieza con el código
  del padre seguido de un punto, y el tipo es el mismo que el del padre.
- Naturaleza: obligatoria en las cuentas imputables (las que reciben movimientos).

Modificación (2.a):
- Las reglas de jerarquía se validan solo si cambian el código, el padre o el tipo, para que las
  cuentas heredadas que no las cumplen puedan seguir editándose sin tocar su ubicación.
- Con cuentas hijas no se puede cambiar el código, el tipo ni el padre, ni marcarla como imputable.
- Con movimientos no se puede cambiar el tipo ni dejar de ser imputable.

Cuentas predeterminadas: deben ser activas, imputables y de tipo y naturaleza coherentes con su uso
(REGLAS_PREDETERMINADA); una cuenta predeterminada no puede modificarse para quedar incoherente.

Baja lógica (2.b): sin movimientos, sin cuentas hijas activas y sin estar configurada como cuenta
predeterminada. La cuenta se marca inactiva y conserva su información histórica.
"""

import re
from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import auditoria
from app.errors import ErrorNegocio
from app.models import (
    CUENTA_NO,
    CUENTA_SI,
    AsientoContable,
    ClavePredeterminada,
    CuentaPredeterminada,
    DetalleAsiento,
    Naturaleza,
    PlanCuenta,
    TipoCuenta,
    Usuario,
)
from app.schemas_plan_cuentas import CuentaIn
from app.tiempo import ahora

TABLA = "PLAN_CUENTA"
TABLA_PREDETERMINADAS = "CUENTA_PREDETERMINADA"
FORMATO_CODIGO = re.compile(r"^\d+(\.\d+)*$")

DESCRIPCION_PREDETERMINADA = {
    ClavePredeterminada.VENTAS: "Ventas",
    ClavePredeterminada.DEUDORES_POR_VENTAS: "Deudores por ventas",
    ClavePredeterminada.IVA_DEBITO_FISCAL: "IVA débito fiscal",
    ClavePredeterminada.COMPRAS: "Compras",
    ClavePredeterminada.PROVEEDORES: "Proveedores",
    ClavePredeterminada.IVA_CREDITO_FISCAL: "IVA crédito fiscal",
    ClavePredeterminada.RESULTADO_EJERCICIO: "Resultado del ejercicio",
}


@dataclass(frozen=True)
class ReglaPredeterminada:
    tipos: tuple[TipoCuenta, ...]
    naturaleza: Naturaleza | None  # None: se admite cualquiera


# Tipo y naturaleza coherentes para cada cuenta predeterminada. Compras admite Activo (inventario
# permanente: Mercaderías) o Gastos (inventario periódico: cuenta Compras). El Resultado del
# ejercicio puede tener saldo deudor o acreedor.
REGLAS_PREDETERMINADA = {
    ClavePredeterminada.VENTAS: ReglaPredeterminada((TipoCuenta.INGRESOS,), Naturaleza.ACREEDORA),
    ClavePredeterminada.DEUDORES_POR_VENTAS: ReglaPredeterminada((TipoCuenta.ACTIVO,), Naturaleza.DEUDORA),
    ClavePredeterminada.IVA_DEBITO_FISCAL: ReglaPredeterminada((TipoCuenta.PASIVO,), Naturaleza.ACREEDORA),
    ClavePredeterminada.COMPRAS: ReglaPredeterminada((TipoCuenta.ACTIVO, TipoCuenta.GASTOS), Naturaleza.DEUDORA),
    ClavePredeterminada.PROVEEDORES: ReglaPredeterminada((TipoCuenta.PASIVO,), Naturaleza.ACREEDORA),
    ClavePredeterminada.IVA_CREDITO_FISCAL: ReglaPredeterminada((TipoCuenta.ACTIVO,), Naturaleza.DEUDORA),
    ClavePredeterminada.RESULTADO_EJERCICIO: ReglaPredeterminada((TipoCuenta.PATRIMONIO_NETO,), None),
}

ETIQUETA_TIPO = {
    TipoCuenta.ACTIVO: "Activo",
    TipoCuenta.PASIVO: "Pasivo",
    TipoCuenta.PATRIMONIO_NETO: "Patrimonio neto",
    TipoCuenta.INGRESOS: "Ingresos",
    TipoCuenta.GASTOS: "Gastos",
}


# ---------- Consulta (paso 1 y 2.c) ----------


def listar(
    db: Session, buscar: str | None, tipo: TipoCuenta | None, activa: bool | None, imputable: bool | None
) -> list[tuple[PlanCuenta, str | None]]:
    """Cuentas ordenadas por código, cada una con el código de su padre."""
    cuentas = list(db.scalars(select(PlanCuenta)))
    codigos = {c.id_cuenta: c.codigo for c in cuentas}
    texto = (buscar or "").strip().lower()
    resultado = [
        (c, codigos.get(c.id_cuenta_padre) if c.id_cuenta_padre else None)
        for c in cuentas
        if (not texto or texto in (c.codigo or "").lower() or texto in (c.nombre or "").lower())
        and (tipo is None or c.tipo_cuenta == tipo)
        and (activa is None or c.esta_activa == activa)
        and (imputable is None or c.es_imputable == imputable)
    ]
    return sorted(resultado, key=lambda par: _orden(par[0].codigo))


def obtener(db: Session, id_cuenta: int) -> PlanCuenta:
    cuenta = db.get(PlanCuenta, id_cuenta)
    if cuenta is None:
        raise ErrorNegocio(404, "La cuenta no existe.")
    return cuenta


def ruta(db: Session, cuenta: PlanCuenta) -> list[PlanCuenta]:
    """Ancestros de la cuenta, desde el rubro principal hasta el padre inmediato."""
    ancestros: list[PlanCuenta] = []
    actual = cuenta
    while actual.id_cuenta_padre is not None and len(ancestros) < 50:
        padre = db.get(PlanCuenta, actual.id_cuenta_padre)
        if padre is None:
            break
        ancestros.insert(0, padre)
        actual = padre
    return ancestros


def cantidad_hijas(db: Session, id_cuenta: int, solo_activas: bool = False) -> int:
    consulta = select(func.count()).select_from(PlanCuenta).where(PlanCuenta.id_cuenta_padre == id_cuenta)
    if solo_activas:
        consulta = consulta.where(PlanCuenta.activo == CUENTA_SI)
    return db.scalar(consulta) or 0


def cantidad_movimientos(db: Session, id_cuenta: int) -> int:
    consulta = select(func.count()).select_from(DetalleAsiento).where(DetalleAsiento.id_cuenta == id_cuenta)
    return db.scalar(consulta) or 0


def movimientos(db: Session, id_cuenta: int) -> list[tuple[DetalleAsiento, AsientoContable]]:
    obtener(db, id_cuenta)
    consulta = (
        select(DetalleAsiento, AsientoContable)
        .join(AsientoContable, AsientoContable.id_asiento == DetalleAsiento.id_asiento)
        .where(DetalleAsiento.id_cuenta == id_cuenta)
        .order_by(AsientoContable.fecha.desc(), AsientoContable.numero_asiento.desc())
    )
    return [(detalle, asiento) for detalle, asiento in db.execute(consulta)]


def predeterminada_para(db: Session, id_cuenta: int) -> list[ClavePredeterminada]:
    consulta = select(CuentaPredeterminada.clave).where(CuentaPredeterminada.id_cuenta == id_cuenta)
    return sorted(ClavePredeterminada(clave) for clave in db.scalars(consulta))


# ---------- Alta y modificación (pasos 2-6 y 2.a) ----------


def validar(db: Session, datos: CuentaIn, id_cuenta: int | None = None) -> None:
    """Pasos 4 / 2.a.3: valida sin guardar. Lanza ErrorNegocio con el problema encontrado."""
    actual = obtener(db, id_cuenta) if id_cuenta is not None else None
    codigo = datos.codigo

    if not FORMATO_CODIGO.match(codigo):
        raise ErrorNegocio(422, "El código debe tener números separados por puntos, por ejemplo 1.1.1.01.")
    duplicada = db.scalar(select(PlanCuenta).where(PlanCuenta.codigo == codigo))
    if duplicada is not None and (actual is None or duplicada.id_cuenta != actual.id_cuenta):  # 4.a
        estado = "" if duplicada.esta_activa else " (dada de baja)"
        raise ErrorNegocio(409, f"El código {codigo} ya está registrado para la cuenta «{duplicada.nombre}»{estado}.")

    if datos.imputable and datos.naturaleza is None:
        raise ErrorNegocio(422, "Indique la naturaleza (deudora o acreedora) de la cuenta imputable.")

    # Las reglas de jerarquía se aplican a las altas y a lo que cambia: una cuenta heredada que no las
    # cumple puede seguir editándose (por ejemplo, su nombre) mientras no se toque su ubicación.
    cambia_ubicacion = actual is None or (
        codigo != actual.codigo
        or datos.id_cuenta_padre != actual.id_cuenta_padre
        or datos.tipo_cuenta != actual.tipo_cuenta
    )
    if cambia_ubicacion:
        _validar_jerarquia(db, datos, actual)  # 4.b

    if actual is not None:
        hijas = cantidad_hijas(db, actual.id_cuenta)
        if hijas:
            if codigo != actual.codigo or datos.tipo_cuenta != actual.tipo_cuenta:
                raise ErrorNegocio(
                    409, "La cuenta tiene cuentas dependientes: no se puede cambiar su código ni su tipo."
                )
            if datos.id_cuenta_padre != actual.id_cuenta_padre:
                raise ErrorNegocio(409, "La cuenta tiene cuentas dependientes: no se puede cambiar su cuenta padre.")
            if datos.imputable and not actual.es_imputable:
                raise ErrorNegocio(409, "Una cuenta con cuentas dependientes no puede ser imputable.")
        if cantidad_movimientos(db, actual.id_cuenta):
            if datos.tipo_cuenta != actual.tipo_cuenta:
                raise ErrorNegocio(409, "La cuenta tiene movimientos: no se puede cambiar su tipo.")
            if not datos.imputable and actual.es_imputable:
                raise ErrorNegocio(409, "La cuenta tiene movimientos: debe seguir siendo imputable.")
        # Una cuenta predeterminada no puede quedar incoherente con el uso que tiene asignado.
        for clave in predeterminada_para(db, actual.id_cuenta):
            if not datos.imputable:
                uso = DESCRIPCION_PREDETERMINADA[clave]
                raise ErrorNegocio(409, f"La cuenta es la predeterminada para «{uso}»: debe seguir siendo imputable.")
            _verificar_coherencia(clave, datos.tipo_cuenta, datos.naturaleza, status_code=409)


def crear(db: Session, datos: CuentaIn, actor: Usuario, origen: str | None) -> PlanCuenta:
    validar(db, datos)
    cuenta = PlanCuenta(activo=CUENTA_SI)
    _aplicar(cuenta, datos)
    db.add(cuenta)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=cuenta.id_cuenta,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(cuenta),
    )
    _confirmar(db)
    return cuenta


def modificar(db: Session, id_cuenta: int, datos: CuentaIn, actor: Usuario, origen: str | None) -> PlanCuenta:
    validar(db, datos, id_cuenta)
    cuenta = obtener(db, id_cuenta)
    antes = _instantanea(cuenta)
    _aplicar(cuenta, datos)
    despues = _instantanea(cuenta)
    if antes != despues:  # 2.a.6
        auditoria.registrar(
            db,
            accion="MODIFICACION",
            tabla=TABLA,
            id_registro=cuenta.id_cuenta,
            actor=actor.email,
            origen=origen,
            antes=antes,
            despues=despues,
        )
    _confirmar(db)
    return cuenta


# ---------- Baja lógica (2.b) y reactivación ----------


def verificar_baja(db: Session, id_cuenta: int) -> PlanCuenta:
    """2.b.1: comprueba que la cuenta pueda darse de baja."""
    cuenta = obtener(db, id_cuenta)
    if not cuenta.esta_activa:
        raise ErrorNegocio(409, "La cuenta ya se encuentra dada de baja.")
    if cantidad_movimientos(db, id_cuenta):
        raise ErrorNegocio(409, "La cuenta tiene movimientos registrados: no puede darse de baja.")
    if cantidad_hijas(db, id_cuenta, solo_activas=True):
        raise ErrorNegocio(409, "La cuenta tiene cuentas dependientes activas: deben darse de baja primero.")
    claves = predeterminada_para(db, id_cuenta)
    if claves:
        nombres = ", ".join(DESCRIPCION_PREDETERMINADA[c] for c in claves)
        raise ErrorNegocio(409, f"La cuenta está configurada como predeterminada para: {nombres}. Reemplácela primero.")
    return cuenta


def dar_de_baja(db: Session, id_cuenta: int, actor: Usuario, origen: str | None) -> PlanCuenta:
    cuenta = verificar_baja(db, id_cuenta)
    antes = _instantanea(cuenta)
    cuenta.activo = CUENTA_NO
    auditoria.registrar(
        db,
        accion="BAJA",
        tabla=TABLA,
        id_registro=cuenta.id_cuenta,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(cuenta),
    )
    _confirmar(db)
    return cuenta


def reactivar(db: Session, id_cuenta: int, actor: Usuario, origen: str | None) -> PlanCuenta:
    cuenta = obtener(db, id_cuenta)
    if cuenta.esta_activa:
        raise ErrorNegocio(409, "La cuenta ya se encuentra activa.")
    if cuenta.id_cuenta_padre is not None:
        padre = db.get(PlanCuenta, cuenta.id_cuenta_padre)
        if padre is None or not padre.esta_activa:
            raise ErrorNegocio(409, "La cuenta padre está dada de baja: reactívela primero.")
    antes = _instantanea(cuenta)
    cuenta.activo = CUENTA_SI
    auditoria.registrar(
        db,
        accion="REACTIVACION",
        tabla=TABLA,
        id_registro=cuenta.id_cuenta,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(cuenta),
    )
    _confirmar(db)
    return cuenta


# ---------- Cuentas predeterminadas ----------


def listar_predeterminadas(db: Session) -> list[tuple[ClavePredeterminada, PlanCuenta | None]]:
    asignadas = {p.clave: p.id_cuenta for p in db.scalars(select(CuentaPredeterminada))}
    resultado = []
    for clave in ClavePredeterminada:
        id_cuenta = asignadas.get(clave)
        resultado.append((clave, db.get(PlanCuenta, id_cuenta) if id_cuenta else None))
    return resultado


def asignar_predeterminada(
    db: Session, clave: ClavePredeterminada, id_cuenta: int | None, actor: Usuario, origen: str | None
) -> PlanCuenta | None:
    cuenta = None
    if id_cuenta is not None:
        cuenta = obtener(db, id_cuenta)
        if not cuenta.esta_activa or not cuenta.es_imputable:
            raise ErrorNegocio(422, "La cuenta predeterminada debe ser una cuenta activa e imputable.")
        _verificar_coherencia(clave, cuenta.tipo_cuenta, cuenta.naturaleza)

    registro = db.get(CuentaPredeterminada, str(clave))
    anterior = registro.id_cuenta if registro else None
    if anterior == id_cuenta:
        return cuenta
    if registro is None:
        registro = CuentaPredeterminada(clave=str(clave))
        db.add(registro)
    registro.id_cuenta = id_cuenta
    registro.fecha_modificacion = ahora()
    registro.usuario = actor.email
    auditoria.registrar(
        db,
        accion="PREDETERMINADA",
        tabla=TABLA_PREDETERMINADAS,
        id_registro=id_cuenta,
        actor=actor.email,
        origen=origen,
        antes={"clave": str(clave), "id_cuenta": anterior},
        despues={"clave": str(clave), "id_cuenta": id_cuenta},
    )
    db.commit()
    return cuenta


# ---------- Auxiliares ----------


def describir_regla(clave: ClavePredeterminada) -> str:
    """Ej.: «Ingresos, naturaleza acreedora» o «Activo o Gastos, naturaleza deudora»."""
    regla = REGLAS_PREDETERMINADA[clave]
    tipos = " o ".join(ETIQUETA_TIPO[t] for t in regla.tipos)
    return f"{tipos}, naturaleza {regla.naturaleza.lower()}" if regla.naturaleza else tipos


def _verificar_coherencia(
    clave: ClavePredeterminada, tipo: str | None, naturaleza: str | None, status_code: int = 422
) -> None:
    regla = REGLAS_PREDETERMINADA[clave]
    # Una naturaleza vacía (cuentas cargadas antes de la migración 003) no se considera incoherente.
    if tipo not in regla.tipos or (regla.naturaleza and naturaleza and naturaleza != regla.naturaleza):
        raise ErrorNegocio(
            status_code,
            f"La cuenta para «{DESCRIPCION_PREDETERMINADA[clave]}» debe ser de tipo {describir_regla(clave)}.",
        )


def _validar_jerarquia(db: Session, datos: CuentaIn, actual: PlanCuenta | None) -> None:
    if datos.id_cuenta_padre is None:
        if "." in datos.codigo:
            raise ErrorNegocio(422, "Una cuenta sin cuenta padre debe tener un código de un solo nivel, por ejemplo 1.")
        return
    if actual is not None and datos.id_cuenta_padre == actual.id_cuenta:
        raise ErrorNegocio(422, "Una cuenta no puede ser su propia cuenta padre.")
    padre = db.get(PlanCuenta, datos.id_cuenta_padre)
    if padre is None:
        raise ErrorNegocio(422, "La cuenta padre indicada no existe.")
    if not padre.esta_activa:
        raise ErrorNegocio(422, f"La cuenta padre {padre.codigo} está dada de baja.")
    if padre.es_imputable:
        raise ErrorNegocio(
            422, f"La cuenta padre {padre.codigo} es imputable: solo los rubros pueden tener cuentas dependientes."
        )
    if not datos.codigo.startswith(f"{padre.codigo}."):
        raise ErrorNegocio(422, f"El código debe comenzar con el de la cuenta padre: {padre.codigo}.")
    if datos.tipo_cuenta != padre.tipo_cuenta:
        raise ErrorNegocio(422, f"El tipo debe coincidir con el de la cuenta padre ({padre.tipo_cuenta}).")


def _aplicar(cuenta: PlanCuenta, datos: CuentaIn) -> None:
    cuenta.codigo = datos.codigo
    cuenta.nombre = datos.nombre
    cuenta.tipo_cuenta = datos.tipo_cuenta
    cuenta.naturaleza = datos.naturaleza
    cuenta.imputable = CUENTA_SI if datos.imputable else CUENTA_NO
    cuenta.id_cuenta_padre = datos.id_cuenta_padre


def _instantanea(cuenta: PlanCuenta) -> dict[str, Any]:
    return {
        "codigo": cuenta.codigo,
        "nombre": cuenta.nombre,
        "tipo_cuenta": cuenta.tipo_cuenta,
        "naturaleza": cuenta.naturaleza,
        "imputable": cuenta.imputable,
        "id_cuenta_padre": cuenta.id_cuenta_padre,
        "activo": cuenta.activo,
    }


def _orden(codigo: str | None) -> tuple[int, ...]:
    try:
        return tuple(int(s) for s in (codigo or "").split("."))
    except ValueError:
        return (10**9,)


def _confirmar(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:  # carrera contra el índice único de código
        db.rollback()
        raise ErrorNegocio(409, "Ya existe una cuenta con ese código.") from exc
