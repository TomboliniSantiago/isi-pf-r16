import { useCallback, useEffect, useMemo, useState } from "react";
import { mensajeDeError } from "../../api/client";
import { TIPOS, etiquetaNaturaleza, etiquetaTipo, planCuentasApi, type Cuenta, type TipoCuenta } from "../../api/planCuentas";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { DetalleCuenta } from "./DetalleCuenta";
import { EstadoCuenta } from "./EstadoCuenta";
import { FormularioCuenta } from "./FormularioCuenta";
import { Predeterminadas } from "./Predeterminadas";

type Dialogo =
  | { tipo: "formulario"; cuenta: Cuenta | null; padre: Cuenta | null }
  | { tipo: "detalle"; idCuenta: number }
  | { tipo: "estado"; cuenta: Cuenta; accion: "baja" | "reactivar" };

type Estado = "activas" | "baja" | "";
type Clase = "" | "imputables" | "rubros";

/** CUU-005 Gestionar Plan de Cuentas. */
export function PlanCuentasPage() {
  const { usuario } = useAuth();
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRADOR";

  const [pestania, setPestania] = useState<"cuentas" | "predeterminadas">("cuentas");
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [buscar, setBuscar] = useState("");
  const [tipo, setTipo] = useState<TipoCuenta | "">("");
  const [estado, setEstado] = useState<Estado>("activas");
  const [clase, setClase] = useState<Clase>("");
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);

  const cargar = useCallback(async () => {
    setCargando(true);
    try {
      setCuentas(await planCuentasApi.listar());
      setError(null);
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  // El plan es chico: se trae completo una vez y se filtra en el navegador.
  const visibles = useMemo(() => {
    const texto = buscar.trim().toLowerCase();
    return cuentas.filter(
      (c) =>
        (!texto || (c.codigo ?? "").toLowerCase().includes(texto) || (c.nombre ?? "").toLowerCase().includes(texto)) &&
        (!tipo || c.tipo_cuenta === tipo) &&
        (estado === "" || c.activa === (estado === "activas")) &&
        (clase === "" || c.imputable === (clase === "imputables")),
    );
  }, [cuentas, buscar, tipo, estado, clase]);

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
          <h1>Plan de cuentas</h1>
          <p className="texto-secundario">Estructura de cuentas contables sobre la que se imputan las operaciones.</p>
        </div>
        {puedeEditar && pestania === "cuentas" && (
          <button
            type="button"
            className="boton boton-primario"
            onClick={() => setDialogo({ tipo: "formulario", cuenta: null, padre: null })}
          >
            + Nueva cuenta
          </button>
        )}
      </div>

      <div className="pestanias" role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={pestania === "cuentas"}
          className={pestania === "cuentas" ? "pestania activa" : "pestania"}
          onClick={() => setPestania("cuentas")}
        >
          Cuentas
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={pestania === "predeterminadas"}
          className={pestania === "predeterminadas" ? "pestania activa" : "pestania"}
          onClick={() => setPestania("predeterminadas")}
        >
          Cuentas predeterminadas
        </button>
      </div>

      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}
      {error && <Alerta tipo="error">{error}</Alerta>}

      {pestania === "predeterminadas" ? (
        <Predeterminadas cuentas={cuentas} puedeEditar={puedeEditar} />
      ) : (
        <section className="tarjeta tarjeta-tabla">
          <div className="filtros filtros-4">
            <label className="campo campo-busqueda">
              <span>Buscar</span>
              <input
                type="search"
                placeholder="Código o denominación"
                value={buscar}
                onChange={(e) => setBuscar(e.target.value)}
              />
            </label>
            <label className="campo">
              <span>Tipo</span>
              <select value={tipo} onChange={(e) => setTipo(e.target.value as TipoCuenta | "")}>
                <option value="">Todos</option>
                {TIPOS.map((t) => (
                  <option key={t.valor} value={t.valor}>
                    {t.etiqueta}
                  </option>
                ))}
              </select>
            </label>
            <label className="campo">
              <span>Clase</span>
              <select value={clase} onChange={(e) => setClase(e.target.value as Clase)}>
                <option value="">Todas</option>
                <option value="rubros">Rubros</option>
                <option value="imputables">Imputables</option>
              </select>
            </label>
            <label className="campo">
              <span>Estado</span>
              <select value={estado} onChange={(e) => setEstado(e.target.value as Estado)}>
                <option value="activas">Vigentes</option>
                <option value="baja">Dadas de baja</option>
                <option value="">Todas</option>
              </select>
            </label>
          </div>

          <div className="tabla-contenedor">
            <table className="tabla tabla-plan">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Denominación</th>
                  <th>Tipo</th>
                  <th>Naturaleza</th>
                  <th>Cuenta padre</th>
                  <th>Estado</th>
                  <th className="col-acciones">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {visibles.map((c) => (
                  <tr key={c.id_cuenta} className={c.imputable ? undefined : "fila-rubro"}>
                    <td className="codigo-cuenta">{c.codigo}</td>
                    <td>
                      <span style={{ paddingLeft: `${(c.nivel - 1) * 1.1}rem` }}>{c.nombre}</span>
                    </td>
                    <td>{etiquetaTipo(c.tipo_cuenta)}</td>
                    <td>{etiquetaNaturaleza(c.naturaleza)}</td>
                    <td className="codigo-cuenta">{c.codigo_padre ?? "—"}</td>
                    <td>
                      {c.activa ? (
                        <span className="etiqueta etiqueta-activo">Vigente</span>
                      ) : (
                        <span className="etiqueta etiqueta-baja">Dada de baja</span>
                      )}
                    </td>
                    <td className="col-acciones">
                      <div className="acciones">
                        <button
                          type="button"
                          className="boton-enlace"
                          onClick={() => setDialogo({ tipo: "detalle", idCuenta: c.id_cuenta })}
                        >
                          Ver
                        </button>
                        {puedeEditar && c.activa && (
                          <>
                            {!c.imputable && (
                              <button
                                type="button"
                                className="boton-enlace"
                                onClick={() => setDialogo({ tipo: "formulario", cuenta: null, padre: c })}
                              >
                                + Subcuenta
                              </button>
                            )}
                            <button
                              type="button"
                              className="boton-enlace"
                              onClick={() => setDialogo({ tipo: "formulario", cuenta: c, padre: null })}
                            >
                              Editar
                            </button>
                            <button
                              type="button"
                              className="boton-enlace boton-enlace-peligro"
                              onClick={() => setDialogo({ tipo: "estado", cuenta: c, accion: "baja" })}
                            >
                              Dar de baja
                            </button>
                          </>
                        )}
                        {puedeEditar && !c.activa && (
                          <button
                            type="button"
                            className="boton-enlace"
                            onClick={() => setDialogo({ tipo: "estado", cuenta: c, accion: "reactivar" })}
                          >
                            Reactivar
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                {!cargando && visibles.length === 0 && (
                  <tr>
                    <td colSpan={7} className="tabla-vacia">
                      {cuentas.length === 0
                        ? "El Plan de Cuentas está vacío. Comience dando de alta los rubros principales (1 Activo, 2 Pasivo, …)."
                        : "No se encontraron cuentas con los filtros seleccionados."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
            {cargando && <div className="tabla-cargando">Cargando…</div>}
          </div>
        </section>
      )}

      {dialogo?.tipo === "formulario" && (
        <FormularioCuenta
          cuentas={cuentas}
          cuenta={dialogo.cuenta}
          padreInicial={dialogo.padre}
          onCerrar={cerrarDialogo}
          onGuardado={informar}
        />
      )}
      {dialogo?.tipo === "detalle" && <DetalleCuenta idCuenta={dialogo.idCuenta} onCerrar={cerrarDialogo} />}
      {dialogo?.tipo === "estado" && (
        <EstadoCuenta cuenta={dialogo.cuenta} accion={dialogo.accion} onCerrar={cerrarDialogo} onListo={informar} />
      )}
    </>
  );
}
