import { useCallback, useEffect, useRef, useState } from "react";
import { CONDICIONES_IVA, clientesApi, type Cliente, type CondicionIva } from "../../api/clientes";
import { mensajeDeError } from "../../api/client";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { AltaCliente } from "./AltaCliente";
import { DetalleCliente } from "./DetalleCliente";
import { EditarCliente } from "./EditarCliente";
import { EstadoCliente } from "./EstadoCliente";

type Dialogo =
  | { tipo: "alta" }
  | { tipo: "editar"; cliente: Cliente }
  | { tipo: "detalle"; idCliente: number }
  | { tipo: "estado"; cliente: Cliente; accion: "baja" | "reactivar" };

type Estado = "activos" | "baja" | "";

/** CUU-007 Gestionar Clientes. */
export function ClientesPage() {
  const { usuario } = useAuth();
  // Actores del caso de uso; el resto de los perfiles solo consulta.
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";

  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [textoBusqueda, setTextoBusqueda] = useState("");
  const [buscar, setBuscar] = useState("");
  const [condicion, setCondicion] = useState<CondicionIva | "">("");
  const [estado, setEstado] = useState<Estado>("activos");
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    const t = setTimeout(() => setBuscar(textoBusqueda.trim()), 300);
    return () => clearTimeout(t);
  }, [textoBusqueda]);

  const cargar = useCallback(async () => {
    const consulta = ++ultimaConsulta.current;
    setCargando(true);
    try {
      const resultado = await clientesApi.listar({
        buscar: buscar || undefined,
        condicion_iva: condicion || undefined,
        activo: estado === "" ? undefined : estado === "activos",
      });
      if (consulta === ultimaConsulta.current) {
        setClientes(resultado);
        setError(null);
      }
    } catch (err) {
      if (consulta === ultimaConsulta.current) setError(mensajeDeError(err));
    } finally {
      if (consulta === ultimaConsulta.current) setCargando(false);
    }
  }, [buscar, condicion, estado]);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const cerrarDialogo = useCallback(() => setDialogo(null), []);

  function informar(mensaje: string) {
    setDialogo(null);
    setExito(mensaje);
    void cargar();
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Clientes</h1>
          <p className="texto-secundario">Alta, modificación, consulta y baja de clientes.</p>
        </div>
        {puedeEditar && (
          <button type="button" className="boton boton-primario" onClick={() => setDialogo({ tipo: "alta" })}>
            + Nuevo cliente
          </button>
        )}
      </div>

      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}

      <section className="tarjeta tarjeta-tabla">
        <div className="filtros">
          <label className="campo campo-busqueda">
            <span>Buscar</span>
            <input
              type="search"
              placeholder="Razón social o CUIT"
              value={textoBusqueda}
              onChange={(e) => setTextoBusqueda(e.target.value)}
            />
          </label>
          <label className="campo">
            <span>Condición IVA</span>
            <select value={condicion} onChange={(e) => setCondicion(e.target.value as CondicionIva | "")}>
              <option value="">Todas</option>
              {CONDICIONES_IVA.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Estado</span>
            <select value={estado} onChange={(e) => setEstado(e.target.value as Estado)}>
              <option value="activos">Activos</option>
              <option value="baja">Dados de baja</option>
              <option value="">Todos</option>
            </select>
          </label>
        </div>

        {error && <Alerta tipo="error">{error}</Alerta>}

        <div className="tabla-contenedor">
          <table className="tabla">
            <thead>
              <tr>
                <th>Código</th>
                <th>Razón social</th>
                <th>CUIT</th>
                <th>Condición IVA</th>
                <th>Localidad</th>
                <th>Estado</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {clientes.map((c) => (
                <tr key={c.id_cliente}>
                  <td className="codigo-cuenta">{c.codigo}</td>
                  <td className="celda-principal">{c.razon_social}</td>
                  <td className="codigo-cuenta">{c.cuit}</td>
                  <td>{c.condicion_iva}</td>
                  <td>{[c.localidad, c.provincia].filter(Boolean).join(", ") || "—"}</td>
                  <td>
                    {c.activo ? (
                      <span className="etiqueta etiqueta-activo">Activo</span>
                    ) : (
                      <span className="etiqueta etiqueta-baja">Dado de baja</span>
                    )}
                  </td>
                  <td className="col-acciones">
                    <div className="acciones">
                      <button
                        type="button"
                        className="boton-enlace"
                        onClick={() => setDialogo({ tipo: "detalle", idCliente: c.id_cliente })}
                      >
                        Ver
                      </button>
                      {puedeEditar && c.activo && (
                        <>
                          <button
                            type="button"
                            className="boton-enlace"
                            onClick={() => setDialogo({ tipo: "editar", cliente: c })}
                          >
                            Editar
                          </button>
                          <button
                            type="button"
                            className="boton-enlace boton-enlace-peligro"
                            onClick={() => setDialogo({ tipo: "estado", cliente: c, accion: "baja" })}
                          >
                            Dar de baja
                          </button>
                        </>
                      )}
                      {puedeEditar && !c.activo && (
                        <button
                          type="button"
                          className="boton-enlace"
                          onClick={() => setDialogo({ tipo: "estado", cliente: c, accion: "reactivar" })}
                        >
                          Reactivar
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {!cargando && clientes.length === 0 && (
                <tr>
                  <td colSpan={7} className="tabla-vacia">
                    No se encontraron clientes con los filtros seleccionados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "alta" && (
        <AltaCliente
          onCerrar={cerrarDialogo}
          onCreado={informar}
          onVerExistente={(c) => setDialogo({ tipo: "detalle", idCliente: c.id_cliente })}
        />
      )}
      {dialogo?.tipo === "editar" && (
        <EditarCliente cliente={dialogo.cliente} onCerrar={cerrarDialogo} onGuardado={informar} />
      )}
      {dialogo?.tipo === "detalle" && <DetalleCliente idCliente={dialogo.idCliente} onCerrar={cerrarDialogo} />}
      {dialogo?.tipo === "estado" && (
        <EstadoCliente cliente={dialogo.cliente} accion={dialogo.accion} onCerrar={cerrarDialogo} onListo={informar} />
      )}
    </>
  );
}
