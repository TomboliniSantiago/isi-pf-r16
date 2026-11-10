import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { mensajeDeError } from "../../api/client";
import type { Proveedor } from "../../api/proveedores";
import { formatearFechaContable, formatearImporte, type Cuenta } from "../../api/planCuentas";
import {
  CONDICIONES_PAGO,
  TIPOS_COMPROBANTE,
  etiquetaEstadoCompra,
  comprasApi,
  type CondicionPago,
  type CuentasCompra,
  type Propuesta,
  type TipoComprobante,
  type Compra,
  type CompraDatos,
} from "../../api/compras";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { AltaProveedor } from "../proveedores/AltaProveedor";

interface Props {
  /** Proveedores vigentes. */
  proveedores: Proveedor[];
  /** Cuentas vigentes e imputables, para elegir las que el sistema no pudo determinar (4.a). */
  cuentas: Cuenta[];
  /** Compra pendiente a modificar; null para una compra nueva. */
  compra: Compra | null;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
  onProveedorCreado: (proveedor: Proveedor) => void;
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
 * CUU-002 Registrar compra, carga manual (1.a): el usuario ingresa el comprobante, el sistema propone el
 * asiento (cuentas según el Plan de Cuentas y la condición de pago) y el usuario lo revisa y confirma.
 */
export function FormularioCompra({ proveedores, cuentas, compra, onCerrar, onGuardado, onProveedorCreado }: Props) {
  const [idProveedor, setIdProveedor] = useState(compra?.proveedor ? String(compra.proveedor.id_proveedor) : "");
  const [tipo, setTipo] = useState<TipoComprobante>((compra?.tipo_comprobante as TipoComprobante) ?? "Factura A");
  const [puntoVenta, setPuntoVenta] = useState(compra?.punto_venta ? String(compra.punto_venta) : "1");
  const [numero, setNumero] = useState(compra?.numero_comprobante ? String(compra.numero_comprobante) : "");
  const [fechaEmision, setFechaEmision] = useState(compra?.fecha_emision ?? hoy());
  const [fechaContable, setFechaContable] = useState(
    compra?.fecha_contable && compra.fecha_contable !== compra.fecha_emision ? compra.fecha_contable : "",
  );
  const [condicion, setCondicion] = useState<CondicionPago>((compra?.condicion_compra as CondicionPago) ?? "Cuenta Corriente");
  const [neto, setNeto] = useState(compra?.importe_neto_gravado ?? "");
  const [iva, setIva] = useState(compra && Number(compra.importe_iva) ? (compra.importe_iva ?? "") : "");
  const [otros, setOtros] = useState(compra && Number(compra.importe_otros_impuestos) ? (compra.importe_otros_impuestos ?? "") : "");
  const [total, setTotal] = useState(compra?.importe_total ?? "");
  const [elegidas, setElegidas] = useState<CuentasCompra>({});
  const [propuesta, setPropuesta] = useState<Propuesta | null>(null);
  const [altaProveedor, setAltaProveedor] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const suma = aCentavos(neto) + aCentavos(iva) + aCentavos(otros);
  const diferencia = aCentavos(total) - suma;
  // Solo la Factura A discrimina IVA (crédito fiscal); en la B y la C el IVA integra el costo.
  const sinIva = tipo !== "Factura A";

  function datos(confirmar: boolean, cuentasElegidas: CuentasCompra = elegidas): CompraDatos {
    return {
      id_proveedor: Number(idProveedor),
      tipo_comprobante: tipo,
      punto_venta: Number(puntoVenta),
      numero_comprobante: Number(numero),
      fecha_emision: fechaEmision,
      fecha_contable: fechaContable || null,
      condicion_compra: condicion,
      importe_neto_gravado: importe(neto),
      importe_iva: sinIva ? "0" : importe(iva),
      importe_otros_impuestos: importe(otros),
      importe_total: importe(total),
      cuentas: cuentasElegidas,
      confirmar,
    };
  }

  function validarFormulario(): string | null {
    if (!idProveedor) return "Seleccione el proveedor.";
    if (!Number.isInteger(Number(puntoVenta)) || Number(puntoVenta) < 1) return "Indique un punto de venta válido.";
    if (!Number.isInteger(Number(numero)) || Number(numero) < 1) return "Indique el número de comprobante.";
    if (!fechaEmision) return "Indique la fecha de emisión.";
    for (const [nombre, valor] of [
      ["neto gravado", neto],
      ["IVA", sinIva ? "" : iva],
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
      setPropuesta(await comprasApi.proponer(datos(true)));
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function elegirCuenta(rol: keyof CuentasCompra, valor: string) {
    const nuevas = { ...elegidas, [rol]: valor ? Number(valor) : null };
    setElegidas(nuevas);
    try {
      setPropuesta(await comprasApi.proponer(datos(true, nuevas)));
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
      const r = compra ? await comprasApi.modificar(compra.id_compra, datos(confirmar)) : await comprasApi.crear(datos(confirmar));
      onGuardado(
        r.estado === "CONTABILIZADA"
          ? `La compra ${r.tipo_comprobante} ${r.numero} fue contabilizada con el asiento N° ${r.asiento?.numero_asiento}.`
          : `La compra ${r.tipo_comprobante} ${r.numero} quedó pendiente de contabilizar.`,
      );
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  if (altaProveedor) {
    return (
      <AltaProveedor
        onCerrar={() => setAltaProveedor(false)}
        onCreado={(_, proveedor) => {
          onProveedorCreado(proveedor);
          setIdProveedor(String(proveedor.id_proveedor));
          setAltaProveedor(false);
        }}
        onVerExistente={(c) => {
          if (c.activo) setIdProveedor(String(c.id_proveedor));
          setAltaProveedor(false);
        }}
      />
    );
  }

  const titulo = compra ? `Modificar compra ${compra.tipo_comprobante} ${compra.numero}` : "Registrar compra";
  const proveedor = proveedores.find((c) => String(c.id_proveedor) === idProveedor);

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
            El comprobante ya fue registrado: compra {propuesta.duplicado.tipo_comprobante} {propuesta.duplicado.numero} a{" "}
            <strong>{propuesta.duplicado.proveedor?.razon_social}</strong> del {formatearFechaContable(propuesta.duplicado.fecha_emision)},
            por {formatearImporte(propuesta.duplicado.importe_total ?? 0)} ({etiquetaEstadoCompra(propuesta.duplicado.estado).toLowerCase()}).
            No se generará el asiento.
          </Alerta>
        )}
        {propuesta.cuentas_faltantes.length > 0 && (
          <Alerta tipo="aviso">
            No se pudo determinar la cuenta de {propuesta.cuentas_faltantes.join(", ")}. Selecciónela en la tabla o configúrela
            como cuenta predeterminada en el <Link to="/plan-cuentas">Plan de Cuentas</Link>; mientras tanto, puede guardar la compra
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
          <dt>Proveedor</dt>
          <dd>
            {proveedor?.razon_social} <span className="texto-secundario">{proveedor?.cuit}</span>
          </dd>
          <dt>Comprobante</dt>
          <dd>
            {tipo} {String(puntoVenta).padStart(4, "0")}-{String(numero).padStart(8, "0")}
          </dd>
          <dt>Fecha de emisión</dt>
          <dd>{formatearFechaContable(fechaEmision)}</dd>
          <dt>Fecha contable</dt>
          <dd>{formatearFechaContable(fechaContable || fechaEmision)}</dd>
          <dt>Condición de pago</dt>
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
            Al confirmar, el asiento se registrará en el Libro Diario y la compra quedará contabilizada.
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
          <button type="submit" form="form-compra" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Validando…" : "Revisar asiento"}
          </button>
        </>
      }
    >
      <form id="form-compra" onSubmit={revisar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <label className="campo">
          <span>Proveedor</span>
          <select value={idProveedor} onChange={(e) => setIdProveedor(e.target.value)} required autoFocus>
            <option value="">— Seleccione el proveedor —</option>
            {proveedores.map((c) => (
              <option key={c.id_proveedor} value={c.id_proveedor}>
                {c.razon_social} · {c.cuit}
              </option>
            ))}
          </select>
        </label>
        <p className="texto-secundario">
          ¿El proveedor no está registrado?{" "}
          <button type="button" className="boton-enlace" onClick={() => setAltaProveedor(true)}>
            Registrar proveedor nuevo
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
            <span>Condición de pago</span>
            <select value={condicion} onChange={(e) => setCondicion(e.target.value as CondicionPago)}>
              {CONDICIONES_PAGO.map((c) => (
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
              value={sinIva ? "" : iva}
              onChange={(e) => setIva(e.target.value)}
              placeholder={sinIva ? "No discrimina" : "0,00"}
              disabled={sinIva}
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
