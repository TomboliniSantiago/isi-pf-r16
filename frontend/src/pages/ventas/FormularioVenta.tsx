import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { mensajeDeError } from "../../api/client";
import type { Cliente } from "../../api/clientes";
import { formatearFechaContable, formatearImporte, type Cuenta } from "../../api/planCuentas";
import {
  CONDICIONES_COBRO,
  TIPOS_COMPROBANTE,
  etiquetaEstadoVenta,
  ventasApi,
  type CondicionCobro,
  type CuentasVenta,
  type Propuesta,
  type TipoComprobante,
  type Venta,
  type VentaDatos,
} from "../../api/ventas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { AltaCliente } from "../clientes/AltaCliente";

interface Props {
  /** Clientes vigentes. */
  clientes: Cliente[];
  /** Cuentas vigentes e imputables, para elegir las que el sistema no pudo determinar (4.a). */
  cuentas: Cuenta[];
  /** Venta pendiente a modificar; null para una venta nueva. */
  venta: Venta | null;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
  onClienteCreado: (cliente: Cliente) => void;
}

function hoy(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function aCentavos(valor: string): number {
  const n = Number((valor || "0").replace(",", "."));
  return Number.isFinite(n) ? Math.round(n * 100) : NaN;
}

const importe = (v: string) => (v ? v.replace(",", ".") : "0");

/**
 * CUU-001 Registrar venta, carga manual (1.a): el usuario ingresa el comprobante, el sistema propone el
 * asiento (cuentas según el Plan de Cuentas y la condición de cobro) y el usuario lo revisa y confirma.
 */
export function FormularioVenta({ clientes, cuentas, venta, onCerrar, onGuardado, onClienteCreado }: Props) {
  const [idCliente, setIdCliente] = useState(venta?.cliente ? String(venta.cliente.id_cliente) : "");
  const [tipo, setTipo] = useState<TipoComprobante>((venta?.tipo_comprobante as TipoComprobante) ?? "Factura A");
  const [puntoVenta, setPuntoVenta] = useState(venta?.punto_venta ? String(venta.punto_venta) : "1");
  const [numero, setNumero] = useState(venta?.numero_comprobante ? String(venta.numero_comprobante) : "");
  const [fechaEmision, setFechaEmision] = useState(venta?.fecha_emision ?? hoy());
  const [fechaContable, setFechaContable] = useState(
    venta?.fecha_contable && venta.fecha_contable !== venta.fecha_emision ? venta.fecha_contable : "",
  );
  const [condicion, setCondicion] = useState<CondicionCobro>((venta?.condicion_venta as CondicionCobro) ?? "Cuenta Corriente");
  const [neto, setNeto] = useState(venta?.importe_neto_gravado ?? "");
  const [iva, setIva] = useState(venta && Number(venta.importe_iva) ? (venta.importe_iva ?? "") : "");
  const [otros, setOtros] = useState(venta && Number(venta.importe_otros_impuestos) ? (venta.importe_otros_impuestos ?? "") : "");
  const [total, setTotal] = useState(venta?.importe_total ?? "");
  const [elegidas, setElegidas] = useState<CuentasVenta>({});
  const [propuesta, setPropuesta] = useState<Propuesta | null>(null);
  const [altaCliente, setAltaCliente] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const suma = aCentavos(neto) + aCentavos(iva) + aCentavos(otros);
  const diferencia = aCentavos(total) - suma;
  const esFacturaC = tipo === "Factura C";

  function datos(confirmar: boolean, cuentasElegidas: CuentasVenta = elegidas): VentaDatos {
    return {
      id_cliente: Number(idCliente),
      tipo_comprobante: tipo,
      punto_venta: Number(puntoVenta),
      numero_comprobante: Number(numero),
      fecha_emision: fechaEmision,
      fecha_contable: fechaContable || null,
      condicion_venta: condicion,
      importe_neto_gravado: importe(neto),
      importe_iva: esFacturaC ? "0" : importe(iva),
      importe_otros_impuestos: importe(otros),
      importe_total: importe(total),
      cuentas: cuentasElegidas,
      confirmar,
    };
  }

  function validarFormulario(): string | null {
    if (!idCliente) return "Seleccione el cliente.";
    if (!Number.isInteger(Number(puntoVenta)) || Number(puntoVenta) < 1) return "Indique un punto de venta válido.";
    if (!Number.isInteger(Number(numero)) || Number(numero) < 1) return "Indique el número de comprobante.";
    if (!fechaEmision) return "Indique la fecha de emisión.";
    for (const [nombre, valor] of [
      ["neto gravado", neto],
      ["IVA", esFacturaC ? "" : iva],
      ["otros impuestos", otros],
      ["total", total],
    ] as const) {
      const c = aCentavos(valor);
      if (Number.isNaN(c) || c < 0) return `El importe de ${nombre} no es válido.`;
    }
    if (aCentavos(neto) <= 0) return "Indique el neto gravado.";
    return null;
  }

  async function revisar(e: FormEvent) {
    e.preventDefault();
    const problema = validarFormulario();
    if (problema) {
      setError(problema);
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      setPropuesta(await ventasApi.proponer(datos(true)));
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function elegirCuenta(rol: keyof CuentasVenta, valor: string) {
    const nuevas = { ...elegidas, [rol]: valor ? Number(valor) : null };
    setElegidas(nuevas);
    try {
      setPropuesta(await ventasApi.proponer(datos(true, nuevas)));
    } catch (err) {
      setError(mensajeDeError(err));
    }
  }

  async function guardar(confirmar: boolean) {
    const problema = validarFormulario();
    if (problema) {
      setError(problema);
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      const r = venta ? await ventasApi.modificar(venta.id_venta, datos(confirmar)) : await ventasApi.crear(datos(confirmar));
      onGuardado(
        r.estado === "CONTABILIZADA"
          ? `La venta ${r.tipo_comprobante} ${r.numero} fue contabilizada con el asiento N° ${r.asiento?.numero_asiento}.`
          : `La venta ${r.tipo_comprobante} ${r.numero} quedó pendiente de contabilizar.`,
      );
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  if (altaCliente) {
    return (
      <AltaCliente
        onCerrar={() => setAltaCliente(false)}
        onCreado={(_, cliente) => {
          onClienteCreado(cliente);
          setIdCliente(String(cliente.id_cliente));
          setAltaCliente(false);
        }}
        onVerExistente={(c) => {
          if (c.activo) setIdCliente(String(c.id_cliente));
          setAltaCliente(false);
        }}
      />
    );
  }

  const titulo = venta ? `Modificar venta ${venta.tipo_comprobante} ${venta.numero}` : "Registrar venta";
  const cliente = clientes.find((c) => String(c.id_cliente) === idCliente);

  if (propuesta) {
    const bloqueada = !!propuesta.duplicado || propuesta.cuentas_faltantes.length > 0 || !propuesta.balanceado;
    return (
      <Modal
        titulo={`${titulo}: revisar asiento`}
        onCerrar={onCerrar}
        ancho
        pie={
          <>
            <button type="button" className="boton boton-secundario" onClick={() => setPropuesta(null)} disabled={enviando}>
              Volver a editar
            </button>
            {!propuesta.duplicado && (
              <button type="button" className="boton boton-secundario" onClick={() => guardar(false)} disabled={enviando}>
                Guardar como pendiente
              </button>
            )}
            <button type="button" className="boton boton-primario" onClick={() => guardar(true)} disabled={enviando || bloqueada}>
              {enviando ? "Registrando…" : "Confirmar contabilización"}
            </button>
          </>
        }
      >
        {error && <Alerta tipo="error">{error}</Alerta>}
        {propuesta.duplicado && (
          <Alerta tipo="error">
            El comprobante ya fue registrado: venta {propuesta.duplicado.tipo_comprobante} {propuesta.duplicado.numero} a{" "}
            <strong>{propuesta.duplicado.cliente?.razon_social}</strong> del {formatearFechaContable(propuesta.duplicado.fecha_emision)},
            por {formatearImporte(propuesta.duplicado.importe_total ?? 0)} ({etiquetaEstadoVenta(propuesta.duplicado.estado).toLowerCase()}).
            No se generará el asiento.
          </Alerta>
        )}
        {propuesta.cuentas_faltantes.length > 0 && (
          <Alerta tipo="aviso">
            No se pudo determinar la cuenta de {propuesta.cuentas_faltantes.join(", ")}. Selecciónela en la tabla o configúrela
            como cuenta predeterminada en el <Link to="/plan-cuentas">Plan de Cuentas</Link>; mientras tanto, puede guardar la venta
            como pendiente.
          </Alerta>
        )}
        {!propuesta.balanceado && (
          <Alerta tipo="aviso">
            El asiento no está balanceado: diferencia de {formatearImporte(Math.abs(Number(propuesta.diferencia)))} entre el Debe
            y el Haber. Revise que el total sea neto + IVA + otros impuestos.
          </Alerta>
        )}
        <dl className="ficha ficha-doble">
          <dt>Cliente</dt>
          <dd>
            {cliente?.razon_social} <span className="texto-secundario">{cliente?.cuit}</span>
          </dd>
          <dt>Comprobante</dt>
          <dd>
            {tipo} {String(puntoVenta).padStart(4, "0")}-{String(numero).padStart(8, "0")}
          </dd>
          <dt>Fecha de emisión</dt>
          <dd>{formatearFechaContable(fechaEmision)}</dd>
          <dt>Fecha contable</dt>
          <dd>{formatearFechaContable(fechaContable || fechaEmision)}</dd>
          <dt>Condición de cobro</dt>
          <dd>{condicion}</dd>
          <dt>Total</dt>
          <dd>{formatearImporte(importe(total))}</dd>
        </dl>
        <div className="tabla-contenedor">
          <table className="tabla tabla-compacta">
            <thead>
              <tr>
                <th>Concepto</th>
                <th>Cuenta</th>
                <th className="col-importe">Debe</th>
                <th className="col-importe">Haber</th>
              </tr>
            </thead>
            <tbody>
              {propuesta.lineas.map((l) => (
                <tr key={l.rol}>
                  <td className={Number(l.haber) ? "cuenta-haber" : undefined}>{l.descripcion}</td>
                  <td>
                    {/* Cuenta determinada por el sistema; si faltaba, el usuario la elige (y puede cambiarla). */}
                    {l.id_cuenta && !elegidas[l.rol] ? (
                      <>
                        <span className="codigo-cuenta">{l.codigo}</span> {l.nombre}
                      </>
                    ) : (
                      <select value={elegidas[l.rol] ?? ""} onChange={(e) => elegirCuenta(l.rol, e.target.value)}>
                        <option value="">— Seleccione una cuenta —</option>
                        {cuentas.map((c) => (
                          <option key={c.id_cuenta} value={c.id_cuenta}>
                            {c.codigo} · {c.nombre}
                          </option>
                        ))}
                      </select>
                    )}
                  </td>
                  <td className="col-importe">{Number(l.debe) ? formatearImporte(l.debe) : ""}</td>
                  <td className="col-importe">{Number(l.haber) ? formatearImporte(l.haber) : ""}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <td colSpan={2}>Totales</td>
                <td className="col-importe">{formatearImporte(propuesta.total_debe)}</td>
                <td className="col-importe">{formatearImporte(propuesta.total_haber)}</td>
              </tr>
            </tfoot>
          </table>
        </div>
        {!bloqueada && (
          <p className="texto-secundario">
            Al confirmar, el asiento se registrará en el Libro Diario y la venta quedará contabilizada.
          </p>
        )}
      </Modal>
    );
  }

  return (
    <Modal
      titulo={titulo}
      onCerrar={onCerrar}
      ancho
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="button" className="boton boton-secundario" onClick={() => guardar(false)} disabled={enviando}>
            Guardar como pendiente
          </button>
          <button type="submit" form="form-venta" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Validando…" : "Revisar asiento"}
          </button>
        </>
      }
    >
      <form id="form-venta" onSubmit={revisar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <label className="campo">
          <span>Cliente</span>
          <select value={idCliente} onChange={(e) => setIdCliente(e.target.value)} required autoFocus>
            <option value="">— Seleccione el cliente —</option>
            {clientes.map((c) => (
              <option key={c.id_cliente} value={c.id_cliente}>
                {c.razon_social} · {c.cuit}
              </option>
            ))}
          </select>
        </label>
        <p className="texto-secundario">
          ¿El cliente no está registrado?{" "}
          <button type="button" className="boton-enlace" onClick={() => setAltaCliente(true)}>
            Registrar cliente nuevo
          </button>
        </p>

        <div className="campos-fila">
          <label className="campo">
            <span>Tipo de comprobante</span>
            <select value={tipo} onChange={(e) => setTipo(e.target.value as TipoComprobante)}>
              {TIPOS_COMPROBANTE.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Punto de venta</span>
            <input inputMode="numeric" value={puntoVenta} onChange={(e) => setPuntoVenta(e.target.value.replace(/\D/g, ""))} maxLength={5} required />
          </label>
          <label className="campo">
            <span>Número</span>
            <input inputMode="numeric" value={numero} onChange={(e) => setNumero(e.target.value.replace(/\D/g, ""))} maxLength={8} required />
          </label>
        </div>

        <div className="campos-fila">
          <label className="campo">
            <span>Fecha de emisión</span>
            <input type="date" value={fechaEmision} onChange={(e) => setFechaEmision(e.target.value)} required />
          </label>
          <label className="campo">
            <span>Fecha contable (opcional)</span>
            <input type="date" value={fechaContable} min={fechaEmision} onChange={(e) => setFechaContable(e.target.value)} />
          </label>
          <label className="campo">
            <span>Condición de cobro</span>
            <select value={condicion} onChange={(e) => setCondicion(e.target.value as CondicionCobro)}>
              {CONDICIONES_COBRO.map((c) => (
                <option key={c.valor} value={c.valor}>
                  {c.valor} ({c.cuenta})
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="campos-fila">
          <label className="campo">
            <span>Neto gravado</span>
            <input inputMode="decimal" value={neto} onChange={(e) => setNeto(e.target.value)} placeholder="0,00" required />
          </label>
          <label className="campo">
            <span>IVA</span>
            <input
              inputMode="decimal"
              value={esFacturaC ? "" : iva}
              onChange={(e) => setIva(e.target.value)}
              placeholder={esFacturaC ? "No discrimina" : "0,00"}
              disabled={esFacturaC}
            />
          </label>
          <label className="campo">
            <span>Otros impuestos</span>
            <input inputMode="decimal" value={otros} onChange={(e) => setOtros(e.target.value)} placeholder="0,00" />
          </label>
          <label className="campo">
            <span>Total</span>
            <input inputMode="decimal" value={total} onChange={(e) => setTotal(e.target.value)} placeholder="0,00" required />
          </label>
        </div>
        <p className={total && diferencia === 0 ? "balance balance-ok" : "balance balance-error"}>
          {!total ? (
            <>
              Neto + IVA + otros impuestos: {formatearImporte((Number.isNaN(suma) ? 0 : suma) / 100)}.{" "}
              {suma > 0 && (
                <button type="button" className="boton-enlace" onClick={() => setTotal(String(suma / 100))}>
                  Usar como total
                </button>
              )}
            </>
          ) : diferencia === 0 ? (
            "El total coincide con neto + IVA + otros impuestos."
          ) : (
            `El total no coincide con neto + IVA + otros impuestos: diferencia de ${formatearImporte(Math.abs(diferencia) / 100)}.`
          )}
        </p>
        <p className="texto-secundario">Moneda: pesos argentinos (ARS).</p>
      </form>
    </Modal>
  );
}
