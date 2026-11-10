import { useState, type FormEvent } from "react";
import { asientosApi, type Asiento, type AsientoDatos, type LineaDatos } from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { formatearImporte, type Cuenta } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  /** Cuentas vigentes e imputables. */
  cuentas: Cuenta[];
  /** Asiento a modificar; null para un asiento nuevo. */
  asiento: Asiento | null;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
}

interface Fila {
  clave: number;
  id_cuenta: string;
  debe: string;
  haber: string;
}

let proximaClave = 1;
const filaVacia = (): Fila => ({ clave: proximaClave++, id_cuenta: "", debe: "", haber: "" });

function aCentavos(valor: string): number {
  const n = Number(valor.replace(",", "."));
  return Number.isFinite(n) ? Math.round(n * 100) : NaN;
}

function hoy(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/**
 * CUU-004 Registrar asiento manual (también la modificación de CUU-003 3.a):
 * el usuario carga fecha, concepto y líneas; el sistema muestra los totales y la diferencia,
 * y antes de contabilizar presenta el asiento completo para su confirmación.
 */
export function FormularioAsiento({ cuentas, asiento, onCerrar, onGuardado }: Props) {
  const [fecha, setFecha] = useState(asiento?.fecha ?? hoy());
  const [concepto, setConcepto] = useState(asiento?.concepto ?? "");
  const [referencia, setReferencia] = useState(asiento?.referencia ?? "");
  const [filas, setFilas] = useState<Fila[]>(
    asiento
      ? asiento.lineas.map((l) => ({
          clave: proximaClave++,
          id_cuenta: String(l.id_cuenta),
          debe: Number(l.debe) ? l.debe : "",
          haber: Number(l.haber) ? l.haber : "",
        }))
      : [filaVacia(), filaVacia()],
  );
  const [revisando, setRevisando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // Una modificación de un asiento vigente se contabiliza siempre (CUU-003 3.a).
  const estabaAsentado = asiento?.estado === "ASENTADO";
  const totalDebe = filas.reduce((s, f) => s + (aCentavos(f.debe || "0") || 0), 0);
  const totalHaber = filas.reduce((s, f) => s + (aCentavos(f.haber || "0") || 0), 0);
  const diferencia = totalDebe - totalHaber;
  const balanceado = diferencia === 0 && totalDebe > 0;

  function cambiarFila(clave: number, cambios: Partial<Fila>) {
    setFilas((prev) => prev.map((f) => (f.clave === clave ? { ...f, ...cambios } : f)));
  }

  function lineas(): LineaDatos[] {
    const importe = (v: string) => (v ? v.replace(",", ".") : "0");
    return filas.map((f) => ({ id_cuenta: Number(f.id_cuenta), debe: importe(f.debe), haber: importe(f.haber) }));
  }

  function datos(confirmar: boolean): AsientoDatos {
    return { fecha, concepto, referencia: referencia.trim() || null, lineas: lineas(), confirmar };
  }

  function validarFormulario(): string | null {
    if (!fecha) return "Indique la fecha del asiento.";
    if (!concepto.trim()) return "Indique el concepto del asiento.";
    for (const [i, f] of filas.entries()) {
      if (!f.id_cuenta) return `Línea ${i + 1}: seleccione una cuenta.`;
      const d = f.debe ? aCentavos(f.debe) : 0;
      const h = f.haber ? aCentavos(f.haber) : 0;
      if (Number.isNaN(d) || Number.isNaN(h) || d < 0 || h < 0) return `Línea ${i + 1}: el importe no es válido.`;
      if ((d > 0) === (h > 0)) return `Línea ${i + 1}: indique un importe en el Debe o en el Haber, no en ambos.`;
    }
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
      const t = await asientosApi.totales(lineas());
      if (!t.balanceado) {
        setError(
          `El asiento no está balanceado: diferencia de ${formatearImporte(Math.abs(Number(t.diferencia)))} entre el Debe y el Haber.`,
        );
        return;
      }
      setRevisando(true);
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function guardar(confirmar: boolean) {
    if (!confirmar) {
      const problema = validarFormulario();
      if (problema) {
        setError(problema);
        return;
      }
    }
    setError(null);
    setEnviando(true);
    try {
      const resultado = asiento
        ? await asientosApi.modificar(asiento.id_asiento, datos(confirmar || estabaAsentado))
        : await asientosApi.crear(datos(confirmar));
      onGuardado(
        resultado.estado === "ASENTADO"
          ? `El asiento N° ${resultado.numero_asiento} se registró en el Libro Diario.${asiento && estabaAsentado ? " El asiento original quedó anulado con su contra-asiento." : ""}`
          : "El asiento se guardó como pendiente.",
      );
    } catch (err) {
      setError(mensajeDeError(err));
      setRevisando(false);
      setEnviando(false);
    }
  }

  const nombreCuenta = (id: string) => {
    const c = cuentas.find((x) => String(x.id_cuenta) === id);
    return c ? `${c.codigo} · ${c.nombre}` : "—";
  };
  const titulo = asiento ? `Modificar asiento ${asiento.numero_asiento ? `N° ${asiento.numero_asiento}` : "pendiente"}` : "Asiento manual";

  if (revisando) {
    return (
      <Modal
        titulo={`${titulo}: confirmar`}
        onCerrar={onCerrar}
        ancho
        pie={
          <>
            <button type="button" className="boton boton-secundario" onClick={() => setRevisando(false)} disabled={enviando}>
              Volver a editar
            </button>
            <button type="button" className="boton boton-primario" onClick={() => guardar(true)} disabled={enviando}>
              {enviando ? "Registrando…" : "Confirmar contabilización"}
            </button>
          </>
        }
      >
        {error && <Alerta tipo="error">{error}</Alerta>}
        {estabaAsentado && (
          <Alerta tipo="aviso">
            El asiento original no se edita: se anulará con un contra-asiento y se registrará uno nuevo con estos datos.
          </Alerta>
        )}
        <dl className="ficha">
          <dt>Fecha</dt>
          <dd>{fecha.split("-").reverse().join("/")}</dd>
          <dt>Concepto</dt>
          <dd>{concepto}</dd>
          <dt>Referencia</dt>
          <dd>{referencia || "—"}</dd>
        </dl>
        <TablaLineas
          filas={filas.map((f) => ({ cuenta: nombreCuenta(f.id_cuenta), debe: f.debe, haber: f.haber, clave: f.clave }))}
          totalDebe={totalDebe}
          totalHaber={totalHaber}
        />
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
          {!estabaAsentado && (
            <button type="button" className="boton boton-secundario" onClick={() => guardar(false)} disabled={enviando}>
              Guardar como pendiente
            </button>
          )}
          <button type="submit" form="form-asiento" className="boton boton-primario" disabled={enviando || !balanceado}>
            {enviando ? "Validando…" : "Revisar y contabilizar"}
          </button>
        </>
      }
    >
      <form id="form-asiento" onSubmit={revisar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <div className="campos-fila">
          <label className="campo">
            <span>Fecha</span>
            <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} required />
          </label>
          <label className="campo">
            <span>Referencia (opcional)</span>
            <input value={referencia} onChange={(e) => setReferencia(e.target.value)} maxLength={255} />
          </label>
        </div>
        <label className="campo">
          <span>Concepto</span>
          <input value={concepto} onChange={(e) => setConcepto(e.target.value)} maxLength={255} required autoFocus />
        </label>

        <div className="tabla-contenedor">
          <table className="tabla tabla-compacta tabla-lineas">
            <thead>
              <tr>
                <th>Cuenta</th>
                <th className="col-importe">Debe</th>
                <th className="col-importe">Haber</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filas.map((f) => (
                <tr key={f.clave}>
                  <td>
                    <select value={f.id_cuenta} onChange={(e) => cambiarFila(f.clave, { id_cuenta: e.target.value })}>
                      <option value="">— Seleccione una cuenta —</option>
                      {cuentas.map((c) => (
                        <option key={c.id_cuenta} value={c.id_cuenta}>
                          {c.codigo} · {c.nombre}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="col-importe">
                    <input
                      inputMode="decimal"
                      value={f.debe}
                      onChange={(e) => cambiarFila(f.clave, { debe: e.target.value, haber: e.target.value ? "" : f.haber })}
                      placeholder="0,00"
                    />
                  </td>
                  <td className="col-importe">
                    <input
                      inputMode="decimal"
                      value={f.haber}
                      onChange={(e) => cambiarFila(f.clave, { haber: e.target.value, debe: e.target.value ? "" : f.debe })}
                      placeholder="0,00"
                    />
                  </td>
                  <td>
                    {filas.length > 2 && (
                      <button
                        type="button"
                        className="boton-enlace boton-enlace-peligro"
                        aria-label="Quitar línea"
                        onClick={() => setFilas((prev) => prev.filter((x) => x.clave !== f.clave))}
                      >
                        Quitar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <td>
                  <button type="button" className="boton-enlace" onClick={() => setFilas((prev) => [...prev, filaVacia()])}>
                    + Agregar línea
                  </button>
                </td>
                <td className="col-importe">{formatearImporte(totalDebe / 100)}</td>
                <td className="col-importe">{formatearImporte(totalHaber / 100)}</td>
                <td />
              </tr>
            </tfoot>
          </table>
        </div>
        <p className={balanceado ? "balance balance-ok" : "balance balance-error"}>
          {balanceado
            ? "El asiento está balanceado."
            : totalDebe === 0 && totalHaber === 0
              ? "Ingrese los importes del Debe y del Haber."
              : `Diferencia entre Debe y Haber: ${formatearImporte(Math.abs(diferencia) / 100)}`}
        </p>
      </form>
    </Modal>
  );
}

export function TablaLineas({
  filas,
  totalDebe,
  totalHaber,
}: {
  filas: { clave: number | string; cuenta: string; debe: string; haber: string }[];
  totalDebe: number;
  totalHaber: number;
}) {
  return (
    <div className="tabla-contenedor">
      <table className="tabla tabla-compacta">
        <thead>
          <tr>
            <th>Cuenta</th>
            <th className="col-importe">Debe</th>
            <th className="col-importe">Haber</th>
          </tr>
        </thead>
        <tbody>
          {filas.map((f) => {
            const debe = aCentavos(f.debe || "0") || 0;
            const haber = aCentavos(f.haber || "0") || 0;
            return (
              <tr key={f.clave}>
                <td className={haber ? "cuenta-haber" : undefined}>{f.cuenta}</td>
                <td className="col-importe">{debe ? formatearImporte(debe / 100) : ""}</td>
                <td className="col-importe">{haber ? formatearImporte(haber / 100) : ""}</td>
              </tr>
            );
          })}
        </tbody>
        <tfoot>
          <tr>
            <td>Totales</td>
            <td className="col-importe">{formatearImporte(totalDebe / 100)}</td>
            <td className="col-importe">{formatearImporte(totalHaber / 100)}</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
