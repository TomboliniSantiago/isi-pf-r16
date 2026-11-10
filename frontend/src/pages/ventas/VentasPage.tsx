import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { mensajeDeError } from "../../api/client";
import { clientesApi, type Cliente } from "../../api/clientes";
import { formatearFechaContable, formatearImporte, planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { ESTADOS_VENTA, etiquetaEstadoVenta, ventasApi, type EstadoVenta, type Venta } from "../../api/ventas";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { AnularVenta } from "./AnularVenta";
import { DetalleVenta } from "./DetalleVenta";
import { FormularioVenta } from "./FormularioVenta";

type Dialogo =
  | { tipo: "formulario"; venta: Venta | null }
  | { tipo: "detalle"; idVenta: number }
  | { tipo: "anular"; venta: Venta };

export const CLASE_ESTADO_VENTA: Record<string, string> = {
  CONTABILIZADA: "etiqueta-activo",
  PENDIENTE: "etiqueta-pendiente",
  ANULADA: "etiqueta-baja",
};

/** CUU-001 Registrar venta: consulta de ventas y acceso al registro manual. */
export function VentasPage() {
  const { usuario } = useAuth();
  // Actores del caso de uso; el resto de los perfiles solo consulta.
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";
  const [parametros, setParametros] = useSearchParams();

  const [ventas, setVentas] = useState<Venta[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [textoBusqueda, setTextoBusqueda] = useState("");
  const [buscar, setBuscar] = useState("");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [estado, setEstado] = useState<EstadoVenta | "">("");
  const [dialogo, setDialogo] = useState<Dialogo | null>(() => {
    const id = Number(parametros.get("venta"));
    return id ? { tipo: "detalle", idVenta: id } : null;
  });
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    clientesApi
      .listar({ activo: true })
      .then(setClientes)
      .catch((err) => setError(mensajeDeError(err)));
    planCuentasApi
      .listar({ activa: true, imputable: true })
      .then(setCuentas)
      .catch((err) => setError(mensajeDeError(err)));
  }, []);

  useEffect(() => {
    const t = setTimeout(() => setBuscar(textoBusqueda.trim()), 300);
    return () => clearTimeout(t);
  }, [textoBusqueda]);

  const cargar = useCallback(async () => {
    const consulta = ++ultimaConsulta.current;
    setCargando(true);
    try {
      const resultado = await ventasApi.listar({
        buscar: buscar || undefined,
        desde: desde || undefined,
        hasta: hasta || undefined,
        estado: estado || undefined,
      });
      if (consulta === ultimaConsulta.current) {
        setVentas(resultado);
        setError(null);
      }
    } catch (err) {
      if (consulta === ultimaConsulta.current) setError(mensajeDeError(err));
    } finally {
      if (consulta === ultimaConsulta.current) setCargando(false);
    }
  }, [buscar, desde, hasta, estado]);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const cerrarDialogo = useCallback(() => {
    setDialogo(null);
    if (parametros.has("venta")) setParametros({}, { replace: true });
  }, [parametros, setParametros]);

  function informar(mensaje: string) {
    cerrarDialogo();
    setExito(mensaje);
    void cargar();
  }

  function agregarCliente(cliente: Cliente) {
    setClientes((prev) =>
      [...prev, cliente].sort((a, b) => (a.razon_social ?? "").localeCompare(b.razon_social ?? "")),
    );
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Ventas</h1>
          <p className="texto-secundario">Comprobantes de venta y su asiento contable.</p>
        </div>
        {puedeEditar && (
          <button
            type="button"
            className="boton boton-primario"
            onClick={() => setDialogo({ tipo: "formulario", venta: null })}
          >
            + Registrar venta
          </button>
        )}
      </div>

      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}

      <section className="tarjeta tarjeta-tabla">
        <div className="filtros filtros-4">
          <label className="campo campo-busqueda">
            <span>Buscar</span>
            <input
              type="search"
              placeholder="Cliente o número (0001-00000123)"
              value={textoBusqueda}
              onChange={(e) => setTextoBusqueda(e.target.value)}
            />
          </label>
          <label className="campo">
            <span>Desde</span>
            <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
          </label>
          <label className="campo">
            <span>Hasta</span>
            <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
          </label>
          <label className="campo">
            <span>Estado</span>
            <select value={estado} onChange={(e) => setEstado(e.target.value as EstadoVenta | "")}>
              <option value="">Todos</option>
              {ESTADOS_VENTA.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </label>
        </div>

        {error && <Alerta tipo="error">{error}</Alerta>}

        <div className="tabla-contenedor">
          <table className="tabla">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Comprobante</th>
                <th>Cliente</th>
                <th>Cobro</th>
                <th className="col-importe">Total</th>
                <th>Estado</th>
                <th>Asiento</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {ventas.map((v) => (
                <tr key={v.id_venta}>
                  <td>{formatearFechaContable(v.fecha_emision)}</td>
                  <td className="codigo-cuenta">
                    {v.tipo_comprobante?.replace("Factura ", "FC ")} {v.numero}
                  </td>
                  <td className="celda-principal">{v.cliente?.razon_social ?? "—"}</td>
                  <td>{v.condicion_venta ?? "—"}</td>
                  <td className="col-importe">{formatearImporte(v.importe_total ?? 0)}</td>
                  <td>
                    <span className={`etiqueta ${CLASE_ESTADO_VENTA[v.estado ?? ""] ?? "etiqueta-neutra"}`}>
                      {etiquetaEstadoVenta(v.estado)}
                    </span>
                  </td>
                  <td className="codigo-cuenta">{v.asiento?.numero_asiento ? `N° ${v.asiento.numero_asiento}` : "—"}</td>
                  <td className="col-acciones">
                    <div className="acciones">
                      <button
                        type="button"
                        className="boton-enlace"
                        onClick={() => setDialogo({ tipo: "detalle", idVenta: v.id_venta })}
                      >
                        Ver
                      </button>
                      {puedeEditar && v.estado === "PENDIENTE" && (
                        <button
                          type="button"
                          className="boton-enlace"
                          onClick={() => setDialogo({ tipo: "formulario", venta: v })}
                        >
                          Revisar
                        </button>
                      )}
                      {puedeEditar && v.estado !== "ANULADA" && !v.cae && (
                        <button
                          type="button"
                          className="boton-enlace boton-enlace-peligro"
                          onClick={() => setDialogo({ tipo: "anular", venta: v })}
                        >
                          Anular
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {!cargando && ventas.length === 0 && (
                <tr>
                  <td colSpan={8} className="tabla-vacia">
                    No hay ventas que coincidan con los filtros.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "formulario" && (
        <FormularioVenta
          clientes={clientes}
          cuentas={cuentas}
          venta={dialogo.venta}
          onCerrar={cerrarDialogo}
          onGuardado={informar}
          onClienteCreado={agregarCliente}
        />
      )}
      {dialogo?.tipo === "detalle" && <DetalleVenta idVenta={dialogo.idVenta} onCerrar={cerrarDialogo} />}
      {dialogo?.tipo === "anular" && (
        <AnularVenta venta={dialogo.venta} onCerrar={cerrarDialogo} onListo={informar} />
      )}
    </>
  );
}
