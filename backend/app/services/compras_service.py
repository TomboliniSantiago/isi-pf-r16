"""CUU-002 Registrar compra (carga manual, camino 1.a). Mismo diseño que CUU-001 Registrar venta.

- Paso 2 / 2.a: un comprobante (proveedor, tipo, punto de venta y número) no puede registrarse dos veces,
  salvo que la compra anterior esté anulada.
- Paso 3 / 3.a / 3.b: en la carga manual el usuario selecciona el proveedor, que debe estar vigente; si no
  existe, lo registra desde Proveedores (CUU-008).
- Paso 4 / 4.a / 4.b: las cuentas del asiento salen de las cuentas predeterminadas del Plan de Cuentas:
    Debe  Compras por el neto gravado, IVA crédito fiscal por el IVA y Otros impuestos de compras por los
          otros impuestos (percepciones sufridas), si los hay.
    Haber según la condición de pago: Contado → Caja, Cuenta Corriente → Proveedores,
          Transferencia → Banco; por el total.
  Si falta alguna, el usuario la elige (CuentasCompraIn) o la configura en el Plan de Cuentas.
- Paso 5 / 5.a: el total debe ser neto + IVA + otros impuestos; si no, el asiento no balancea y la compra
  solo puede guardarse pendiente de revisión.
- Pasos 6-7 / 6.a: la compra se contabiliza (asiento asentado en el Libro Diario) o queda PENDIENTE, sin
  asiento ni efecto contable.
- Validaciones fiscales mínimas: solo la Factura A discrimina IVA (en la B y la C el IVA integra el costo);
  un proveedor Responsable Inscripto emite Facturas A o B, y uno Monotributista o Exento, Factura C.
- Sin edición destructiva: solo se modifica una compra pendiente. Anular una compra contabilizada revierte
  su asiento con un contra-asiento.
"""

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app import auditoria
from app.errors import ErrorNegocio
from app.models import (
    AsientoContable,
    ClavePredeterminada,
    Compra,
    CondicionIva,
    EstadoCompra,
    OrigenAsiento,
    Proveedor,
    Usuario,
)
from app.schemas_asientos import AsientoIn, LineaIn
from app.schemas_compras import CompraIn, CuentasCompraIn
from app.schemas_comprobantes import CondicionPago, TipoComprobante
from app.services import asientos_service
from app.services.comprobantes import (
    CERO,
    MONEDA,
    LineaPropuesta,
    Propuesta,
    SelectorCuentas,
    empresa_emisora,
    errores_de_importes,
    filtro_por_numero,
    mensaje_faltantes,
)

TABLA = "COMPRA"

CUENTA_DE_PAGO = {
    CondicionPago.CONTADO: ClavePredeterminada.CAJA,
    CondicionPago.CUENTA_CORRIENTE: ClavePredeterminada.PROVEEDORES,
    CondicionPago.TRANSFERENCIA: ClavePredeterminada.BANCO,
}
DESCRIPCION_PAGO = {
    CondicionPago.CONTADO: "Caja",
    CondicionPago.CUENTA_CORRIENTE: "Proveedores",
    CondicionPago.TRANSFERENCIA: "Banco",
}
TIPOS_POR_PROVEEDOR = {
    CondicionIva.RESPONSABLE_INSCRIPTO: (TipoComprobante.FACTURA_A, TipoComprobante.FACTURA_B),
    CondicionIva.MONOTRIBUTO: (TipoComprobante.FACTURA_C,),
    CondicionIva.EXENTO: (TipoComprobante.FACTURA_C,),
}


# ---------- Consulta (paso 8) ----------


def listar(
    db: Session,
    desde: date | None,
    hasta: date | None,
    id_proveedor: int | None,
    estado: EstadoCompra | None,
    buscar: str | None,
    limite: int = 500,
) -> list[Compra]:
    consulta = select(Compra)
    if desde:
        consulta = consulta.where(Compra.fecha_emision >= desde)
    if hasta:
        consulta = consulta.where(Compra.fecha_emision <= hasta)
    if id_proveedor:
        consulta = consulta.where(Compra.id_proveedor == id_proveedor)
    if estado:
        consulta = consulta.where(Compra.estado == estado)
    if buscar and buscar.strip():
        texto = buscar.strip()
        filtros = [
            Compra.id_proveedor.in_(select(Proveedor.id_proveedor).where(Proveedor.razon_social.ilike(f"%{texto}%")))
        ]
        por_numero = filtro_por_numero(texto, Compra.punto_venta, Compra.numero_comprobante)
        if por_numero is not None:
            filtros.append(por_numero)
        consulta = consulta.where(or_(*filtros))
    consulta = consulta.order_by(Compra.fecha_emision.desc(), Compra.id_compra.desc()).limit(limite)
    return list(db.scalars(consulta))


def obtener(db: Session, id_compra: int) -> Compra:
    compra = db.get(Compra, id_compra)
    if compra is None:
        raise ErrorNegocio(404, "La compra no existe.")
    return compra


def asientos_de(db: Session, ids_compra: list[int]) -> dict[int, AsientoContable]:
    """Para cada compra, el último asiento generado por ella (el vigente o, si se anuló, el revertido)."""
    if not ids_compra:
        return {}
    consulta = (
        select(AsientoContable)
        .where(AsientoContable.id_compra.in_(ids_compra), AsientoContable.tipo_origen == OrigenAsiento.COMPRA)
        .order_by(AsientoContable.id_asiento)
    )
    return {a.id_compra: a for a in db.scalars(consulta) if a.id_compra is not None}


def buscar_duplicado(db: Session, datos: CompraIn, excluir: int | None = None) -> Compra | None:
    """Paso 2 / 2.a: mismo proveedor, tipo, punto de venta y número, y no anulada."""
    consulta = select(Compra).where(
        Compra.id_proveedor == datos.id_proveedor,
        Compra.tipo_comprobante == datos.tipo_comprobante,
        Compra.punto_venta == datos.punto_venta,
        Compra.numero_comprobante == datos.numero_comprobante,
        or_(Compra.estado != EstadoCompra.ANULADA, Compra.estado.is_(None)),
    )
    if excluir is not None:
        consulta = consulta.where(Compra.id_compra != excluir)
    return db.scalars(consulta.limit(1)).first()


# ---------- Validación y asiento propuesto (pasos 2-6) ----------


def proponer(db: Session, datos: CompraIn) -> tuple[Propuesta, Compra | None]:
    """Valida los datos y devuelve el asiento propuesto y, si existe, la compra duplicada. No guarda nada."""
    _validar(db, datos)
    return _propuesta(db, datos), buscar_duplicado(db, datos)


def _validar(db: Session, datos: CompraIn) -> Proveedor:
    empresa_emisora(db)
    proveedor = db.get(Proveedor, datos.id_proveedor)
    if proveedor is None:
        raise ErrorNegocio(422, "El proveedor no existe.")
    if not proveedor.esta_activo:
        raise ErrorNegocio(422, f"El proveedor {proveedor.razon_social} está dado de baja.")
    permitidos = TIPOS_POR_PROVEEDOR.get(proveedor.condicion_iva)  # type: ignore[call-overload]
    if permitidos and datos.tipo_comprobante not in permitidos:
        raise ErrorNegocio(
            422,
            f"Un proveedor {proveedor.condicion_iva} no emite {datos.tipo_comprobante}: "
            f"corresponde {' o '.join(permitidos)}.",
        )
    if datos.tipo_comprobante != TipoComprobante.FACTURA_A and datos.importe_iva > 0:
        raise ErrorNegocio(
            422,
            f"La {datos.tipo_comprobante} no discrimina IVA: el IVA integra el costo y debe informarse en cero.",
        )
    error = errores_de_importes(datos.importe_neto_gravado, datos.fecha_emision, datos.fecha_contable)
    if error:
        raise ErrorNegocio(422, error)
    return proveedor


def _propuesta(db: Session, datos: CompraIn) -> Propuesta:
    """Pasos 4-5: cuentas intervinientes e importes. Las cuentas elegidas por el usuario tienen prioridad."""
    cuenta = SelectorCuentas(db).cuenta
    elegidas = datos.cuentas
    condicion = CondicionPago(datos.condicion_compra)
    lineas = [
        LineaPropuesta(
            "compras",
            "Compras",
            cuenta(elegidas.compras, ClavePredeterminada.COMPRAS),
            datos.importe_neto_gravado,
            CERO,
        ),
    ]
    if datos.importe_iva > 0:
        lineas.append(
            LineaPropuesta(
                "iva",
                "IVA crédito fiscal",
                cuenta(elegidas.iva, ClavePredeterminada.IVA_CREDITO_FISCAL),
                datos.importe_iva,
                CERO,
            )
        )
    if datos.importe_otros_impuestos > 0:
        lineas.append(
            LineaPropuesta(
                "otros_impuestos",
                "Otros impuestos de compras",
                cuenta(elegidas.otros_impuestos, ClavePredeterminada.OTROS_IMPUESTOS_COMPRAS),
                datos.importe_otros_impuestos,
                CERO,
            )
        )
    lineas.append(
        LineaPropuesta(
            "pago",
            DESCRIPCION_PAGO[condicion],
            cuenta(elegidas.pago, CUENTA_DE_PAGO[condicion]),
            CERO,
            datos.importe_total,
        )
    )
    return Propuesta(lineas)


# ---------- Alta, modificación y contabilización ----------


def crear(db: Session, datos: CompraIn, actor: Usuario, origen: str | None) -> Compra:
    proveedor = _validar(db, datos)
    _rechazar_duplicado(db, datos)
    emisor = empresa_emisora(db)
    compra = Compra(id_emisor=emisor.id_emisor, moneda=MONEDA, cotizacion=Decimal("1"), estado=EstadoCompra.PENDIENTE)
    _aplicar(compra, datos)
    db.add(compra)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=compra.id_compra,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(compra),
    )
    if datos.confirmar:
        _contabilizar(db, compra, datos, proveedor, actor, origen)
    asientos_service.confirmar_transaccion(db)
    return compra


def modificar(db: Session, id_compra: int, datos: CompraIn, actor: Usuario, origen: str | None) -> Compra:
    """Solo una compra pendiente (sin asiento) se modifica; una contabilizada se anula y se registra de nuevo."""
    compra = obtener(db, id_compra)
    if compra.estado != EstadoCompra.PENDIENTE:
        raise ErrorNegocio(
            409, "Solo se modifican compras pendientes. Una compra contabilizada se anula y se registra nuevamente."
        )
    proveedor = _validar(db, datos)
    _rechazar_duplicado(db, datos, excluir=compra.id_compra)
    antes = _instantanea(compra)
    _aplicar(compra, datos)
    auditoria.registrar(
        db,
        accion="MODIFICACION",
        tabla=TABLA,
        id_registro=compra.id_compra,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(compra),
    )
    if datos.confirmar:
        _contabilizar(db, compra, datos, proveedor, actor, origen)
    asientos_service.confirmar_transaccion(db)
    return compra


def contabilizar(db: Session, id_compra: int, cuentas: CuentasCompraIn, actor: Usuario, origen: str | None) -> Compra:
    """Pasos 6-7 para una compra pendiente: valida de nuevo y genera el asiento."""
    compra = obtener(db, id_compra)
    if compra.estado != EstadoCompra.PENDIENTE:
        raise ErrorNegocio(409, "Solo se contabilizan compras pendientes.")
    datos = _datos_de(compra, cuentas)
    proveedor = _validar(db, datos)
    _rechazar_duplicado(db, datos, excluir=compra.id_compra)
    _contabilizar(db, compra, datos, proveedor, actor, origen)
    asientos_service.confirmar_transaccion(db)
    return compra


def anular(db: Session, id_compra: int, actor: Usuario, origen: str | None) -> Compra:
    """Una compra pendiente se anula sin efecto contable; una contabilizada, revirtiendo su asiento."""
    compra = obtener(db, id_compra)
    if compra.estado == EstadoCompra.ANULADA:
        raise ErrorNegocio(409, "La compra ya está anulada.")
    antes = _instantanea(compra)
    if compra.estado == EstadoCompra.CONTABILIZADA:
        asiento = asientos_de(db, [compra.id_compra]).get(compra.id_compra)
        if asiento is None:
            raise ErrorNegocio(409, "No se encontró el asiento de la compra.")
        asientos_service.revertir_de_comprobante(db, asiento, actor, origen)
    compra.estado = EstadoCompra.ANULADA
    auditoria.registrar(
        db,
        accion="ANULACION",
        tabla=TABLA,
        id_registro=compra.id_compra,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(compra),
    )
    asientos_service.confirmar_transaccion(db)
    return compra


# ---------- Auxiliares ----------


def _rechazar_duplicado(db: Session, datos: CompraIn, excluir: int | None = None) -> None:
    duplicado = buscar_duplicado(db, datos, excluir)
    if duplicado:
        raise ErrorNegocio(
            409,
            f"El comprobante {duplicado.tipo_comprobante} {duplicado.numero} de este proveedor ya fue registrado "
            f"(compra del {duplicado.fecha_emision:%d/%m/%Y}, {(duplicado.estado or '').lower()}).",
        )


def _contabilizar(
    db: Session, compra: Compra, datos: CompraIn, proveedor: Proveedor, actor: Usuario, origen: str | None
) -> None:
    propuesta = _propuesta(db, datos)
    if propuesta.faltantes:  # 4.a / 4.b
        raise ErrorNegocio(422, mensaje_faltantes(propuesta.faltantes))
    lineas = [
        LineaIn(id_cuenta=linea.cuenta.id_cuenta, debe=linea.debe, haber=linea.haber)
        for linea in propuesta.lineas
        if linea.cuenta is not None
    ]
    asiento = asientos_service.registrar_de_comprobante(
        db,
        AsientoIn(
            fecha=compra.fecha_contable or compra.fecha_emision or date.today(),
            concepto=f"Compra {compra.tipo_comprobante} {compra.numero} {proveedor.razon_social or ''}".strip()[:255],
            referencia=f"{compra.tipo_comprobante} {compra.numero}",
            lineas=lineas,
            confirmar=True,  # valida partida doble (5.a)
        ),
        actor,
        origen,
        OrigenAsiento.COMPRA,
        id_compra=compra.id_compra,
    )
    antes = _instantanea(compra)
    compra.estado = EstadoCompra.CONTABILIZADA
    auditoria.registrar(
        db,
        accion="CONTABILIZACION",
        tabla=TABLA,
        id_registro=compra.id_compra,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues={**_instantanea(compra), "asiento": asiento.numero_asiento},
    )


def _aplicar(compra: Compra, datos: CompraIn) -> None:
    compra.id_proveedor = datos.id_proveedor
    compra.tipo_comprobante = datos.tipo_comprobante
    compra.punto_venta = datos.punto_venta
    compra.numero_comprobante = datos.numero_comprobante
    compra.fecha_emision = datos.fecha_emision
    compra.fecha_contable = datos.fecha_contable or datos.fecha_emision
    compra.condicion_compra = datos.condicion_compra
    compra.importe_neto_gravado = datos.importe_neto_gravado
    compra.importe_iva = datos.importe_iva
    compra.importe_otros_impuestos = datos.importe_otros_impuestos
    compra.importe_total = datos.importe_total


def _datos_de(compra: Compra, cuentas: CuentasCompraIn) -> CompraIn:
    try:
        return CompraIn(
            id_proveedor=compra.id_proveedor,
            tipo_comprobante=compra.tipo_comprobante,
            punto_venta=compra.punto_venta,
            numero_comprobante=compra.numero_comprobante,
            fecha_emision=compra.fecha_emision,
            fecha_contable=compra.fecha_contable,
            condicion_compra=compra.condicion_compra,
            importe_neto_gravado=compra.importe_neto_gravado or CERO,
            importe_iva=compra.importe_iva or CERO,
            importe_otros_impuestos=compra.importe_otros_impuestos or CERO,
            importe_total=compra.importe_total or CERO,
            cuentas=cuentas,
            confirmar=True,
        )
    except ValueError as exc:  # datos cargados antes de CUU-002 que no cumplen las reglas actuales
        raise ErrorNegocio(
            422, "La compra tiene datos incompletos o inválidos: modifíquela antes de contabilizarla."
        ) from exc


def _instantanea(compra: Compra) -> dict[str, Any]:
    return {
        "id_proveedor": compra.id_proveedor,
        "comprobante": f"{compra.tipo_comprobante} {compra.numero}",
        "fecha_emision": compra.fecha_emision,
        "fecha_contable": compra.fecha_contable,
        "condicion_compra": compra.condicion_compra,
        "neto": str(compra.importe_neto_gravado),
        "iva": str(compra.importe_iva),
        "otros_impuestos": str(compra.importe_otros_impuestos),
        "total": str(compra.importe_total),
        "estado": compra.estado,
    }
