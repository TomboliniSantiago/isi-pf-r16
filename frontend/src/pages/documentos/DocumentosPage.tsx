import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { mensajeDeError } from "../../api/client";
import { clientesApi, type Cliente } from "../../api/clientes";
import { comprasApi, type Compra } from "../../api/compras";
import {
  ESTADOS_DOCUMENTO,
  documentosApi,
  etiquetaEstadoDocumento,
  type Documento,
  type DocumentoResumen,
  type EstadoDocumento,
  type OperacionDocumento,
} from "../../api/documentos";
import { formatearImporte, planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { proveedoresApi, type Proveedor } from "../../api/proveedores";
import { ventasApi, type Venta } from "../../api/ventas";
import { useAuth } from "../../auth/AuthContext";
import { Alerta } from "../../components/Alerta";
import { FormularioCompra } from "../compras/FormularioCompra";
import { FormularioVenta } from "../ventas/FormularioVenta";
import { CargaDocumento } from "./CargaDocumento";
import { DetalleDocumento } from "./DetalleDocumento";
import { RevisionDocumento } from "./RevisionDocumento";

type Dialogo =
  | { tipo: "carga" }
  | { tipo: "revision"; documento: Documento }
  | { tipo: "detalle"; documento: Documento }
  | { tipo: "compra"; compra: Compra }
  | { tipo: "venta"; venta: Venta };

const CLASE_ESTADO: Record<string, string> = {
  PENDIENTE_REVISION: "etiqueta-pendiente",
  REGISTRADO: "etiqueta-activo",
  DESCARTADO: "etiqueta-baja",
};

function formatearFechaHora(valor: string | null): string {
  if (!valor) return "—";
  const fecha = new Date(valor.endsWith("Z") || valor.includes("+") ? valor : `${valor}Z`);
  return fecha.toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" });
}

/**
 * CUU-016 Registrar comprobante con OCR/NLP:
 * cargar → extraer → revisar → corregir → registrar (borrador) → revisar el asiento y contabilizar.
 */
export function DocumentosPage() {
  const { usuario } = useAuth();
  const puedeEditar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";
  const [parametros, setParametros] = useSearchParams();

  const [documentos, setDocumentos] = useState<DocumentoResumen[]>([]);
  const [proveedores, setProveedores] = useState<Proveedor[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [estado, setEstado] = useState<EstadoDocumento | "">("");
  const [operacion, setOperacion] = useState<OperacionDocumento | "">("");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    Promise.all([
      proveedoresApi.listar({ activo: true }),
      clientesApi.listar({ activo: true }),
      planCuentasApi.listar({ activa: true, imputable: true }),
    ])
      .then(([p, c, cu]) => {
        setProveedores(p);
        setClientes(c);
        setCuentas(cu);
      })
      .catch((err) => setError(mensajeDeError(err)));
  }, []);

  const cargar = useCallback(async () => {
    const consulta = ++ultimaConsulta.current;
    setCargando(true);
    try {
      const resultado = await documentosApi.listar({ estado: estado || undefined, operacion: operacion || undefined });
      if (consulta === ultimaConsulta.current) {
        setDocumentos(resultado);
        setError(null);
      }
    } catch (err) {
      if (consulta === ultimaConsulta.current) setError(mensajeDeError(err));
    } finally {
      if (consulta === ultimaConsulta.current) setCargando(false);
    }
  }, [estado, operacion]);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const abrir = useCallback(
    async (id: number) => {
      try {
        const documento = await documentosApi.obtener(id);
        setDialogo({
          tipo: documento.estado === "PENDIENTE_REVISION" && puedeEditar ? "revision" : "detalle",
          documento,
        });
      } catch (err) {
        setError(mensajeDeError(err));
      }
    },
    [puedeEditar],
  );

  useEffect(() => {
    const id = Number(parametros.get("documento"));
    if (id) void abrir(id);
  }, [parametros, abrir]);

  const cerrarDialogo = useCallback(() => {
    setDialogo(null);
    if (parametros.has("documento")) setParametros({}, { replace: true });
  }, [parametros, setParametros]);

  function informar(mensaje: string) {
    cerrarDialogo();
    setExito(mensaje);
    void cargar();
  }

  /** Registrado el borrador, se abre la compra o venta para revisar su asiento y contabilizarla (CUU-001/002). */
  async function alRegistrar(documento: Documento) {
    void cargar();
    const comprobante = documento.comprobante;
    if (!comprobante) return informar("El comprobante fue registrado.");
    try {
      if (comprobante.tabla === "COMPRA") setDialogo({ tipo: "compra", compra: await comprasApi.obtener(comprobante.id) });
      else setDialogo({ tipo: "venta", venta: await ventasApi.obtener(comprobante.id) });
      setExito("El comprobante fue registrado como pendiente. Revise el asiento propuesto para contabilizarlo.");
    } catch (err) {
      setError(mensajeDeError(err));
      setDialogo(null);
    }
  }

  function agregarContraparte(contraparte: Proveedor | Cliente) {
    if ("id_proveedor" in contraparte) setProveedores((prev) => [...prev, contraparte]);
    else setClientes((prev) => [...prev, contraparte]);
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Comprobantes digitales</h1>
          <p className="texto-secundario">
            Carga de facturas en PDF o imagen: el sistema extrae los datos, usted los revisa y registra la compra o venta.
          </p>
        </div>
        {puedeEditar && (
          <button type="button" className="boton boton-primario" onClick={() => setDialogo({ tipo: "carga" })}>
            + Cargar comprobante
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
          <label className="campo">
            <span>Estado</span>
            <select value={estado} onChange={(e) => setEstado(e.target.value as EstadoDocumento | "")}>
              <option value="">Todos</option>
              {ESTADOS_DOCUMENTO.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Operación</span>
            <select value={operacion} onChange={(e) => setOperacion(e.target.value as OperacionDocumento | "")}>
              <option value="">Todas</option>
              <option value="COMPRA">Compras</option>
              <option value="VENTA">Ventas</option>
            </select>
          </label>
        </div>

        {error && <Alerta tipo="error">{error}</Alerta>}

        <div className="tabla-contenedor">
          <table className="tabla">
            <thead>
              <tr>
                <th>Cargado</th>
                <th>Archivo</th>
                <th>Operación</th>
                <th>Comprobante</th>
                <th>Contraparte</th>
                <th className="col-importe">Total</th>
                <th>Estado</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {documentos.map((d) => (
                <tr key={d.id_documento}>
                  <td>{formatearFechaHora(d.fecha_carga)}</td>
                  <td className="celda-principal">{d.nombre_archivo}</td>
                  <td>{d.operacion === "COMPRA" ? "Compra" : "Venta"}</td>
                  <td className="codigo-cuenta">{d.numero ? `${d.tipo_comprobante?.replace("Factura ", "FC ") ?? ""} ${d.numero}` : "—"}</td>
                  <td>{d.razon_social ?? "—"}</td>
                  <td className="col-importe">{d.importe_total ? formatearImporte(d.importe_total) : "—"}</td>
                  <td>
                    <span className={`etiqueta ${CLASE_ESTADO[d.estado ?? ""] ?? "etiqueta-neutra"}`}>
                      {etiquetaEstadoDocumento(d.estado)}
                    </span>
                  </td>
                  <td className="col-acciones">
                    <div className="acciones">
                      <button type="button" className="boton-enlace" onClick={() => abrir(d.id_documento)}>
                        {d.estado === "PENDIENTE_REVISION" && puedeEditar ? "Revisar" : "Ver"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {!cargando && documentos.length === 0 && (
                <tr>
                  <td colSpan={8} className="tabla-vacia">
                    No hay comprobantes digitales cargados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "carga" && (
        <CargaDocumento
          onCerrar={cerrarDialogo}
          onCargado={(documento) => {
            void cargar();
            setDialogo({ tipo: "revision", documento });
          }}
        />
      )}
      {dialogo?.tipo === "revision" && (
        <RevisionDocumento
          documento={dialogo.documento}
          contrapartes={dialogo.documento.operacion === "COMPRA" ? proveedores : clientes}
          onCerrar={cerrarDialogo}
          onRegistrado={alRegistrar}
          onDescartado={informar}
          onContraparteCreada={agregarContraparte}
        />
      )}
      {dialogo?.tipo === "detalle" && <DetalleDocumento documento={dialogo.documento} onCerrar={cerrarDialogo} />}
      {dialogo?.tipo === "compra" && (
        <FormularioCompra
          proveedores={proveedores}
          cuentas={cuentas}
          compra={dialogo.compra}
          onCerrar={cerrarDialogo}
          onGuardado={informar}
          onProveedorCreado={(p) => setProveedores((prev) => [...prev, p])}
        />
      )}
      {dialogo?.tipo === "venta" && (
        <FormularioVenta
          clientes={clientes}
          cuentas={cuentas}
          venta={dialogo.venta}
          onCerrar={cerrarDialogo}
          onGuardado={informar}
          onClienteCreado={(c) => setClientes((prev) => [...prev, c])}
        />
      )}
    </>
  );
}
