import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  ESTADOS,
  ORIGENES,
  asientosApi,
  esGestionable,
  etiquetaEstado,
  etiquetaOrigen,
  type Asiento,
  type EstadoAsiento,
  type OrigenAsiento,
} from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { formatearFechaContable, formatearImporte, planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { AccionAsiento } from "./AccionAsiento";
import { FormularioAsiento } from "./FormularioAsiento";

type Dialogo =
  | { tipo: "formulario"; asiento: Asiento | null }
  | { tipo: "accion"; asiento: Asiento; accion: "anular" | "confirmar" };

const CLASE_ESTADO: Record<string, string> = {
  ASENTADO: "etiqueta-activo",
  BORRADOR: "etiqueta-pendiente",
  ANULADO: "etiqueta-baja",
};

/** CUU-003 Gestionar Libro Diario (y acceso a CUU-004 Registrar asiento manual). */
export function LibroDiarioPage() {
  const { usuario } = useAuth();
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";

  const [asientos, setAsientos] = useState<Asiento[]>([]);
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [idCuenta, setIdCuenta] = useState("");
  const [origen, setOrigen] = useState<OrigenAsiento | "">("");
  const [estado, setEstado] = useState<EstadoAsiento | "">("");
  const [abiertos, setAbiertos] = useState<Set<number>>(new Set());
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    planCuentasApi
      .listar({ activa: true, imputable: true })
      .then(setCuentas)
      .catch((err) => setError(mensajeDeError(err)));
  }, []);

  const cargar = useCallback(async () => {
    const consulta = ++ultimaConsulta.current;
    setCargando(true);
    try {
      const resultado = await asientosApi.listar({
        desde: desde || undefined,
        hasta: hasta || undefined,
        id_cuenta: idCuenta ? Number(idCuenta) : undefined,
        tipo_origen: origen || undefined,
        estado: estado || undefined,
      });
      if (consulta === ultimaConsulta.current) {
        setAsientos(resultado);
        setError(null);
      }
    } catch (err) {
      if (consulta === ultimaConsulta.current) setError(mensajeDeError(err));
    } finally {
      if (consulta === ultimaConsulta.current) setCargando(false);
    }
  }, [desde, hasta, idCuenta, origen, estado]);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const cerrarDialogo = useCallback(() => setDialogo(null), []);

  function informar(mensaje: string) {
    setDialogo(null);
    setExito(mensaje);
    void cargar();
  }

  function alternar(id: number) {
    setAbiertos((prev) => {
      const nuevo = new Set(prev);
      if (nuevo.has(id)) nuevo.delete(id);
      else nuevo.add(id);
      return nuevo;
    });
  }

  // CUU-003 2.a / 2.b: mensaje según el filtro que dejó la consulta vacía.
  const mensajeVacio = idCuenta
    ? "No existen movimientos registrados para la cuenta seleccionada."
    : desde || hasta
      ? "No existen movimientos registrados para el período seleccionado."
      : "No hay asientos que coincidan con los filtros.";

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Libro Diario</h1>
          <p className="texto-secundario">Asientos contables registrados, con su detalle de cuentas e importes.</p>
        </div>
        {puedeEditar && (
          <button
            type="button"
            className="boton boton-primario"
            onClick={() => setDialogo({ tipo: "formulario", asiento: null })}
          >
            + Asiento manual
          </button>
        )}
      </div>

      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}

      <section className="tarjeta tarjeta-tabla">
        <div className="filtros filtros-diario">
          <label className="campo">
            <span>Desde</span>
            <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
          </label>
          <label className="campo">
            <span>Hasta</span>
            <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
          </label>
          <label className="campo">
            <span>Cuenta</span>
            <select value={idCuenta} onChange={(e) => setIdCuenta(e.target.value)}>
              <option value="">Todas</option>
              {cuentas.map((c) => (
                <option key={c.id_cuenta} value={c.id_cuenta}>
                  {c.codigo} · {c.nombre}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Tipo</span>
            <select value={origen} onChange={(e) => setOrigen(e.target.value as OrigenAsiento | "")}>
              <option value="">Todos</option>
              {ORIGENES.map((o) => (
                <option key={o.valor} value={o.valor}>
                  {o.etiqueta}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Estado</span>
            <select value={estado} onChange={(e) => setEstado(e.target.value as EstadoAsiento | "")}>
              <option value="">Todos</option>
              {ESTADOS.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </label>
        </div>

        {error && <Alerta tipo="error">{error}</Alerta>}

        <div className="tabla-contenedor">
          <table className="tabla tabla-diario">
            <thead>
              <tr>
                <th>N°</th>
                <th>Fecha</th>
                <th>Concepto</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th className="col-importe">Importe</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            {asientos.map((a) => (
              <tbody key={a.id_asiento} className="asiento">
                <tr className="asiento-cabecera">
                  <td className="codigo-cuenta">{a.numero_asiento ?? "—"}</td>
                  <td>{formatearFechaContable(a.fecha)}</td>
                  <td>
                    <button type="button" className="boton-enlace asiento-concepto" onClick={() => alternar(a.id_asiento)}>
                      {abiertos.has(a.id_asiento) ? "▾" : "▸"} {a.concepto}
                    </button>
                    {a.referencia && <small className="texto-secundario asiento-referencia">{a.referencia}</small>}
                    {a.id_venta && (
                      <small className="asiento-referencia">
                        <Link to={`/ventas?venta=${a.id_venta}`}>Ver comprobante de venta</Link>
                      </small>
                    )}
                    {a.revierte_a && <small className="texto-secundario asiento-referencia">Revierte el asiento N° {a.revierte_a}</small>}
                    {a.revertido_por && (
                      <small className="texto-secundario asiento-referencia">Revertido por el asiento N° {a.revertido_por}</small>
                    )}
                  </td>
                  <td>{etiquetaOrigen(a.tipo_origen)}</td>
                  <td>
                    <span className={`etiqueta ${CLASE_ESTADO[a.estado ?? ""] ?? "etiqueta-neutra"}`}>{etiquetaEstado(a.estado)}</span>
                  </td>
                  <td className="col-importe">{formatearImporte(a.total_debe)}</td>
                  <td className="col-acciones">
                    <div className="acciones">
                      {puedeEditar && a.estado === "BORRADOR" && (
                        <button
                          type="button"
                          className="boton-enlace"
                          onClick={() => setDialogo({ tipo: "accion", asiento: a, accion: "confirmar" })}
                        >
                          Contabilizar
                        </button>
                      )}
                      {puedeEditar && esGestionable(a) && (
                        <>
                          <button
                            type="button"
                            className="boton-enlace"
                            onClick={() => setDialogo({ tipo: "formulario", asiento: a })}
                          >
                            Modificar
                          </button>
                          <button
                            type="button"
                            className="boton-enlace boton-enlace-peligro"
                            onClick={() => setDialogo({ tipo: "accion", asiento: a, accion: "anular" })}
                          >
                            {a.estado === "BORRADOR" ? "Descartar" : "Anular"}
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
                {abiertos.has(a.id_asiento) &&
                  a.lineas.map((l) => (
                    <tr key={l.id_detalle_asiento} className="asiento-linea">
                      <td />
                      <td />
                      <td colSpan={3} className={Number(l.haber) ? "cuenta-haber" : undefined}>
                        <span className="codigo-cuenta">{l.codigo}</span> {l.nombre}
                      </td>
                      <td className="col-importe">
                        {Number(l.debe) ? `D ${formatearImporte(l.debe)}` : `H ${formatearImporte(l.haber)}`}
                      </td>
                      <td />
                    </tr>
                  ))}
              </tbody>
            ))}
            {!cargando && asientos.length === 0 && (
              <tbody>
                <tr>
                  <td colSpan={7} className="tabla-vacia">
                    {mensajeVacio}
                  </td>
                </tr>
              </tbody>
            )}
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "formulario" && (
        <FormularioAsiento cuentas={cuentas} asiento={dialogo.asiento} onCerrar={cerrarDialogo} onGuardado={informar} />
      )}
      {dialogo?.tipo === "accion" && (
        <AccionAsiento asiento={dialogo.asiento} accion={dialogo.accion} onCerrar={cerrarDialogo} onListo={informar} />
      )}
    </>
  );
}
