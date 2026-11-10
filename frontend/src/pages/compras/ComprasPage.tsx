import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { mensajeDeError } from "../../api/client";
import { proveedoresApi, type Proveedor } from "../../api/proveedores";
import { formatearFechaContable, formatearImporte, planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { ESTADOS_COMPRA, etiquetaEstadoCompra, comprasApi, type EstadoCompra, type Compra } from "../../api/compras";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { AnularCompra } from "./AnularCompra";
import { DetalleCompra } from "./DetalleCompra";
import { FormularioCompra } from "./FormularioCompra";

type Dialogo =
  | { tipo: "formulario"; compra: Compra | null }
  | { tipo: "detalle"; idCompra: number }
  | { tipo: "anular"; compra: Compra };

export const CLASE_ESTADO_COMPRA: Record<string, string> = {
  CONTABILIZADA: "etiqueta-activo",
  PENDIENTE: "etiqueta-pendiente",
  ANULADA: "etiqueta-baja",
};

/** CUU-002 Registrar compra: consulta de compras y acceso al registro manual. */
export function ComprasPage() {
  const { usuario } = useAuth();
  // Actores del caso de uso; el resto de los perfiles solo consulta.
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";
  const [parametros, setParametros] = useSearchParams();

  const [compras, setCompras] = useState<Compra[]>([]);
  const [proveedores, setProveedores] = useState<Proveedor[]>([]);
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [textoBusqueda, setTextoBusqueda] = useState("");
  const [buscar, setBuscar] = useState("");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [estado, setEstado] = useState<EstadoCompra | "">("");
  const [dialogo, setDialogo] = useState<Dialogo | null>(() => {
    const id = Number(parametros.get("compra"));
    return id ? { tipo: "detalle", idCompra: id } : null;
  });
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    proveedoresApi
      .listar({ activo: true })
      .then(setProveedores)
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
      const resultado = await comprasApi.listar({
        buscar: buscar || undefined,
        desde: desde || undefined,
        hasta: hasta || undefined,
        estado: estado || undefined,
      });
      if (consulta === ultimaConsulta.current) {
        setCompras(resultado);
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
    if (parametros.has("compra")) setParametros({}, { replace: true });
  }, [parametros, setParametros]);

  function informar(mensaje: string) {
    cerrarDialogo();
    setExito(mensaje);
    void cargar();
  }

  function agregarProveedor(proveedor: Proveedor) {
    setProveedores((prev) =>
      [...prev, proveedor].sort((a, b) => (a.razon_social ?? "").localeCompare(b.razon_social ?? "")),
    );
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Compras</h1>
          <p className="texto-secundario">Comprobantes de compra de proveedores y su asiento contable.</p>
        </div>
        {puedeEditar && (
          <button
            type="button"
            className="boton boton-primario"
            onClick={() => setDialogo({ tipo: "formulario", compra: null })}
          >
            + Registrar compra
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
              placeholder="Proveedor o número (0001-00000123)"
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
            <select value={estado} onChange={(e) => setEstado(e.target.value as EstadoCompra | "")}>
              <option value="">Todos</option>
              {ESTADOS_COMPRA.map((e) => (
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
                <th>Proveedor</th>
                <th>Pago</th>
                <th className="col-importe">Total</th>
                <th>Estado</th>
                <th>Asiento</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {compras.map((v) => (
                <tr key={v.id_compra}>
                  <td>{formatearFechaContable(v.fecha_emision)}</td>
                  <td className="codigo-cuenta">
                    {v.tipo_comprobante?.replace("Factura ", "FC ")} {v.numero}
                  </td>
                  <td className="celda-principal">{v.proveedor?.razon_social ?? "—"}</td>
                  <td>{v.condicion_compra ?? "—"}</td>
                  <td className="col-importe">{formatearImporte(v.importe_total ?? 0)}</td>
                  <td>
                    <span className={`etiqueta ${CLASE_ESTADO_COMPRA[v.estado ?? ""] ?? "etiqueta-neutra"}`}>
                      {etiquetaEstadoCompra(v.estado)}
                    </span>
                  </td>
                  <td className="codigo-cuenta">{v.asiento?.numero_asiento ? `N° ${v.asiento.numero_asiento}` : "—"}</td>
                  <td className="col-acciones">
                    <div className="acciones">
                      <button
                        type="button"
                        className="boton-enlace"
                        onClick={() => setDialogo({ tipo: "detalle", idCompra: v.id_compra })}
                      >
                        Ver
                      </button>
                      {puedeEditar && v.estado === "PENDIENTE" && (
                        <button
                          type="button"
                          className="boton-enlace"
                          onClick={() => setDialogo({ tipo: "formulario", compra: v })}
                        >
                          Revisar
                        </button>
                      )}
                      {puedeEditar && v.estado !== "ANULADA" && (
                        <button
                          type="button"
                          className="boton-enlace boton-enlace-peligro"
                          onClick={() => setDialogo({ tipo: "anular", compra: v })}
                        >
                          Anular
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {!cargando && compras.length === 0 && (
                <tr>
                  <td colSpan={8} className="tabla-vacia">
                    No hay compras que coincidan con los filtros.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "formulario" && (
        <FormularioCompra
          proveedores={proveedores}
          cuentas={cuentas}
          compra={dialogo.compra}
          onCerrar={cerrarDialogo}
          onGuardado={informar}
          onProveedorCreado={agregarProveedor}
        />
      )}
      {dialogo?.tipo === "detalle" && <DetalleCompra idCompra={dialogo.idCompra} onCerrar={cerrarDialogo} />}
      {dialogo?.tipo === "anular" && (
        <AnularCompra compra={dialogo.compra} onCerrar={cerrarDialogo} onListo={informar} />
      )}
    </>
  );
}
