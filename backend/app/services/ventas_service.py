"""CUU-001 Registrar venta (carga manual, camino 1.a).

- Paso 2 / 2.a: un comprobante (tipo, punto de venta y número de la empresa emisora) no puede registrarse
  dos veces, salvo que la venta anterior esté anulada.
- Paso 3 / 3.a / 3.b: en la carga manual el usuario selecciona el cliente, que debe estar vigente; si no
  existe, lo registra desde Clientes (CUU-007).
- Paso 4 / 4.a / 4.b: las cuentas del asiento salen de las cuentas predeterminadas del Plan de Cuentas:
    Debe  según la condición de cobro: Contado → Caja, Cuenta Corriente → Deudores por ventas,
          Transferencia → Banco; por el total.
    Haber Ventas por el neto gravado, IVA débito fiscal por el IVA y Otros impuestos de ventas por los
          otros impuestos (percepciones), si los hay.
  Si falta alguna, el usuario la elige (CuentasVentaIn) o la configura en el Plan de Cuentas.
- Paso 5 / 5.a: el total debe ser neto + IVA + otros impuestos; si no, el asiento no balancea y la venta
  solo puede guardarse pendiente de revisión.
- Pasos 6-7 / 6.a: la venta se contabiliza (asiento asentado en el Libro Diario) o queda PENDIENTE, sin
  asiento ni efecto contable.
- Validaciones fiscales mínimas: la Factura C no discrimina IVA; un emisor Responsable Inscripto emite
  Facturas A o B, y uno Monotributista o Exento, Factura C.
- Sin edición destructiva: solo se modifica una venta pendiente. Anular una venta contabilizada revierte
  su asiento con un contra-asiento. Una venta con CAE no se anula (requiere una nota de crédito).
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
    Cliente,
    CondicionIva,
    EmpresaEmisora,
    EstadoVenta,
    OrigenAsiento,
    Usuario,
    Venta,
)
from app.schemas_asientos import AsientoIn, LineaIn
from app.schemas_comprobantes import CondicionPago, TipoComprobante
from app.schemas_ventas import CuentasVentaIn, VentaIn
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

TABLA = "VENTA"

CUENTA_DE_COBRO = {
    CondicionPago.CONTADO: ClavePredeterminada.CAJA,
    CondicionPago.CUENTA_CORRIENTE: ClavePredeterminada.DEUDORES_POR_VENTAS,
    CondicionPago.TRANSFERENCIA: ClavePredeterminada.BANCO,
}
DESCRIPCION_COBRO = {
    CondicionPago.CONTADO: "Caja",
    CondicionPago.CUENTA_CORRIENTE: "Deudores por ventas",
    CondicionPago.TRANSFERENCIA: "Banco",
}
TIPOS_POR_EMISOR = {
    CondicionIva.RESPONSABLE_INSCRIPTO: (TipoComprobante.FACTURA_A, TipoComprobante.FACTURA_B),
    CondicionIva.MONOTRIBUTO: (TipoComprobante.FACTURA_C,),
    CondicionIva.EXENTO: (TipoComprobante.FACTURA_C,),
}


# ---------- Consulta (paso 8) ----------


def listar(
    db: Session,
    desde: date | None,
    hasta: date | None,
    id_cliente: int | None,
    estado: EstadoVenta | None,
    buscar: str | None,
    limite: int = 500,
) -> list[Venta]:
    consulta = select(Venta)
    if desde:
        consulta = consulta.where(Venta.fecha_emision >= desde)
    if hasta:
        consulta = consulta.where(Venta.fecha_emision <= hasta)
    if id_cliente:
        consulta = consulta.where(Venta.id_cliente == id_cliente)
    if estado:
        consulta = consulta.where(Venta.estado == estado)
    if buscar and buscar.strip():
        texto = buscar.strip()
        filtros = [Venta.id_cliente.in_(select(Cliente.id_cliente).where(Cliente.razon_social.ilike(f"%{texto}%")))]
        por_numero = filtro_por_numero(texto, Venta.punto_venta, Venta.numero_comprobante)
        if por_numero is not None:
            filtros.append(por_numero)
        consulta = consulta.where(or_(*filtros))
    consulta = consulta.order_by(Venta.fecha_emision.desc(), Venta.id_venta.desc()).limit(limite)
    return list(db.scalars(consulta))


def obtener(db: Session, id_venta: int) -> Venta:
    venta = db.get(Venta, id_venta)
    if venta is None:
        raise ErrorNegocio(404, "La venta no existe.")
    return venta


def asientos_de(db: Session, ids_venta: list[int]) -> dict[int, AsientoContable]:
    """Para cada venta, el último asiento generado por ella (el vigente o, si se anuló, el revertido)."""
    if not ids_venta:
        return {}
    consulta = (
        select(AsientoContable)
        .where(AsientoContable.id_venta.in_(ids_venta), AsientoContable.tipo_origen == OrigenAsiento.VENTA)
        .order_by(AsientoContable.id_asiento)
    )
    return {a.id_venta: a for a in db.scalars(consulta) if a.id_venta is not None}


def buscar_duplicado(db: Session, datos: VentaIn, id_emisor: int, excluir: int | None = None) -> Venta | None:
    """Paso 2 / 2.a: misma empresa emisora, tipo, punto de venta y número, y no anulada."""
    consulta = select(Venta).where(
        Venta.id_emisor == id_emisor,
        Venta.tipo_comprobante == datos.tipo_comprobante,
        Venta.punto_venta == datos.punto_venta,
        Venta.numero_comprobante == datos.numero_comprobante,
        or_(Venta.estado != EstadoVenta.ANULADA, Venta.estado.is_(None)),
    )
    if excluir is not None:
        consulta = consulta.where(Venta.id_venta != excluir)
    return db.scalars(consulta.limit(1)).first()


# ---------- Validación y asiento propuesto (pasos 2-6) ----------


def proponer(db: Session, datos: VentaIn) -> tuple[Propuesta, Venta | None]:
    """Valida los datos y devuelve el asiento propuesto y, si existe, la venta duplicada. No guarda nada."""
    emisor, cliente = _validar(db, datos)
    return _propuesta(db, datos), buscar_duplicado(db, datos, emisor.id_emisor)


def _validar(db: Session, datos: VentaIn) -> tuple[EmpresaEmisora, Cliente]:
    emisor = empresa_emisora(db)
    cliente = db.get(Cliente, datos.id_cliente)
    if cliente is None:
        raise ErrorNegocio(422, "El cliente no existe.")
    if not cliente.esta_activo:
        raise ErrorNegocio(422, f"El cliente {cliente.razon_social} está dado de baja.")
    permitidos = TIPOS_POR_EMISOR.get(emisor.condicion_iva)  # type: ignore[call-overload]
    if permitidos and datos.tipo_comprobante not in permitidos:
        raise ErrorNegocio(
            422,
            f"Un emisor {emisor.condicion_iva} no emite {datos.tipo_comprobante}: "
            f"corresponde {' o '.join(permitidos)}.",
        )
    if datos.tipo_comprobante == TipoComprobante.FACTURA_C and datos.importe_iva > 0:
        raise ErrorNegocio(422, "La Factura C no discrimina IVA: el importe de IVA debe ser cero.")
    error = errores_de_importes(datos.importe_neto_gravado, datos.fecha_emision, datos.fecha_contable)
    if error:
        raise ErrorNegocio(422, error)
    return emisor, cliente


def _propuesta(db: Session, datos: VentaIn) -> Propuesta:
    """Paso 4-5: cuentas intervinientes e importes. Las cuentas elegidas por el usuario tienen prioridad."""
    cuenta = SelectorCuentas(db).cuenta
    elegidas = datos.cuentas
    condicion = CondicionPago(datos.condicion_venta)
    lineas = [
        LineaPropuesta(
            "cobro",
            DESCRIPCION_COBRO[condicion],
            cuenta(elegidas.cobro, CUENTA_DE_COBRO[condicion]),
            datos.importe_total,
            CERO,
        ),
        LineaPropuesta(
            "ventas", "Ventas", cuenta(elegidas.ventas, ClavePredeterminada.VENTAS), CERO, datos.importe_neto_gravado
        ),
    ]
    if datos.importe_iva > 0:
        lineas.append(
            LineaPropuesta(
                "iva",
                "IVA débito fiscal",
                cuenta(elegidas.iva, ClavePredeterminada.IVA_DEBITO_FISCAL),
                CERO,
                datos.importe_iva,
            )
        )
    if datos.importe_otros_impuestos > 0:
        lineas.append(
            LineaPropuesta(
                "otros_impuestos",
                "Otros impuestos de ventas",
                cuenta(elegidas.otros_impuestos, ClavePredeterminada.OTROS_IMPUESTOS_VENTAS),
                CERO,
                datos.importe_otros_impuestos,
            )
        )
    return Propuesta(lineas)


# ---------- Alta, modificación y contabilización ----------


def crear(db: Session, datos: VentaIn, actor: Usuario, origen: str | None, confirmar_transaccion: bool = True) -> Venta:
    """confirmar_transaccion=False: lo guarda en la transacción en curso (lo usa el registro desde un
    comprobante digital, CUU-016, que guarda en la misma transacción el documento y sus correcciones)."""
    emisor, cliente = _validar(db, datos)
    _rechazar_duplicado(db, datos, emisor.id_emisor)
    venta = Venta(id_emisor=emisor.id_emisor, moneda=MONEDA, cotizacion=Decimal("1"), estado=EstadoVenta.PENDIENTE)
    _aplicar(venta, datos)
    db.add(venta)
    db.flush()
    auditoria.registrar(
        db,
        accion="ALTA",
        tabla=TABLA,
        id_registro=venta.id_venta,
        actor=actor.email,
        origen=origen,
        despues=_instantanea(venta),
    )
    if datos.confirmar:
        _contabilizar(db, venta, datos, cliente, actor, origen)
    if confirmar_transaccion:
        asientos_service.confirmar_transaccion(db)
    return venta


def modificar(db: Session, id_venta: int, datos: VentaIn, actor: Usuario, origen: str | None) -> Venta:
    """Solo una venta pendiente (sin asiento) se modifica; una contabilizada se anula y se registra de nuevo."""
    venta = obtener(db, id_venta)
    if venta.estado != EstadoVenta.PENDIENTE:
        raise ErrorNegocio(
            409, "Solo se modifican ventas pendientes. Una venta contabilizada se anula y se registra nuevamente."
        )
    emisor, cliente = _validar(db, datos)
    _rechazar_duplicado(db, datos, emisor.id_emisor, excluir=venta.id_venta)
    antes = _instantanea(venta)
    _aplicar(venta, datos)
    auditoria.registrar(
        db,
        accion="MODIFICACION",
        tabla=TABLA,
        id_registro=venta.id_venta,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(venta),
    )
    if datos.confirmar:
        _contabilizar(db, venta, datos, cliente, actor, origen)
    asientos_service.confirmar_transaccion(db)
    return venta


def contabilizar(db: Session, id_venta: int, cuentas: CuentasVentaIn, actor: Usuario, origen: str | None) -> Venta:
    """Pasos 6-7 para una venta pendiente: valida de nuevo y genera el asiento."""
    venta = obtener(db, id_venta)
    if venta.estado != EstadoVenta.PENDIENTE:
        raise ErrorNegocio(409, "Solo se contabilizan ventas pendientes.")
    datos = _datos_de(venta, cuentas)
    emisor, cliente = _validar(db, datos)
    _rechazar_duplicado(db, datos, emisor.id_emisor, excluir=venta.id_venta)
    _contabilizar(db, venta, datos, cliente, actor, origen)
    asientos_service.confirmar_transaccion(db)
    return venta


def anular(db: Session, id_venta: int, actor: Usuario, origen: str | None) -> Venta:
    """Una venta pendiente se anula sin efecto contable; una contabilizada, revirtiendo su asiento."""
    venta = obtener(db, id_venta)
    if venta.estado == EstadoVenta.ANULADA:
        raise ErrorNegocio(409, "La venta ya está anulada.")
    if venta.cae:
        raise ErrorNegocio(409, "La venta tiene CAE de ARCA: para anularla debe emitirse una nota de crédito.")
    antes = _instantanea(venta)
    if venta.estado == EstadoVenta.CONTABILIZADA:
        asiento = asientos_de(db, [venta.id_venta]).get(venta.id_venta)
        if asiento is None:
            raise ErrorNegocio(409, "No se encontró el asiento de la venta.")
        asientos_service.revertir_de_comprobante(db, asiento, actor, origen)
    venta.estado = EstadoVenta.ANULADA
    auditoria.registrar(
        db,
        accion="ANULACION",
        tabla=TABLA,
        id_registro=venta.id_venta,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues=_instantanea(venta),
    )
    asientos_service.confirmar_transaccion(db)
    return venta


# ---------- Auxiliares ----------


def _rechazar_duplicado(db: Session, datos: VentaIn, id_emisor: int, excluir: int | None = None) -> None:
    duplicado = buscar_duplicado(db, datos, id_emisor, excluir)
    if duplicado:
        raise ErrorNegocio(
            409,
            f"El comprobante {duplicado.tipo_comprobante} {duplicado.numero} ya fue registrado "
            f"(venta del {duplicado.fecha_emision:%d/%m/%Y}, {(duplicado.estado or '').lower()}).",
        )


def _contabilizar(
    db: Session, venta: Venta, datos: VentaIn, cliente: Cliente, actor: Usuario, origen: str | None
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
            fecha=venta.fecha_contable or venta.fecha_emision or date.today(),
            concepto=f"Venta {venta.tipo_comprobante} {venta.numero} {cliente.razon_social or ''}".strip()[:255],
            referencia=f"{venta.tipo_comprobante} {venta.numero}",
            lineas=lineas,
            confirmar=True,  # valida partida doble (5.a)
        ),
        actor,
        origen,
        OrigenAsiento.VENTA,
        id_venta=venta.id_venta,
    )
    antes = _instantanea(venta)
    venta.estado = EstadoVenta.CONTABILIZADA
    auditoria.registrar(
        db,
        accion="CONTABILIZACION",
        tabla=TABLA,
        id_registro=venta.id_venta,
        actor=actor.email,
        origen=origen,
        antes=antes,
        despues={**_instantanea(venta), "asiento": asiento.numero_asiento},
    )


def _aplicar(venta: Venta, datos: VentaIn) -> None:
    venta.id_cliente = datos.id_cliente
    venta.tipo_comprobante = datos.tipo_comprobante
    venta.punto_venta = datos.punto_venta
    venta.numero_comprobante = datos.numero_comprobante
    venta.fecha_emision = datos.fecha_emision
    venta.fecha_contable = datos.fecha_contable or datos.fecha_emision
    venta.condicion_venta = datos.condicion_venta
    venta.importe_neto_gravado = datos.importe_neto_gravado
    venta.importe_iva = datos.importe_iva
    venta.importe_otros_impuestos = datos.importe_otros_impuestos
    venta.importe_total = datos.importe_total


def _datos_de(venta: Venta, cuentas: CuentasVentaIn) -> VentaIn:
    try:
        return VentaIn(
            id_cliente=venta.id_cliente,
            tipo_comprobante=venta.tipo_comprobante,
            punto_venta=venta.punto_venta,
            numero_comprobante=venta.numero_comprobante,
            fecha_emision=venta.fecha_emision,
            fecha_contable=venta.fecha_contable,
            condicion_venta=venta.condicion_venta,
            importe_neto_gravado=venta.importe_neto_gravado or CERO,
            importe_iva=venta.importe_iva or CERO,
            importe_otros_impuestos=venta.importe_otros_impuestos or CERO,
            importe_total=venta.importe_total or CERO,
            cuentas=cuentas,
            confirmar=True,
        )
    except ValueError as exc:  # datos cargados antes de CUU-001 que no cumplen las reglas actuales
        raise ErrorNegocio(
            422, "La venta tiene datos incompletos o inválidos: modifíquela antes de contabilizarla."
        ) from exc


def _instantanea(venta: Venta) -> dict[str, Any]:
    return {
        "id_cliente": venta.id_cliente,
        "comprobante": f"{venta.tipo_comprobante} {venta.numero}",
        "fecha_emision": venta.fecha_emision,
        "fecha_contable": venta.fecha_contable,
        "condicion_venta": venta.condicion_venta,
        "neto": str(venta.importe_neto_gravado),
        "iva": str(venta.importe_iva),
        "otros_impuestos": str(venta.importe_otros_impuestos),
        "total": str(venta.importe_total),
        "estado": venta.estado,
    }
