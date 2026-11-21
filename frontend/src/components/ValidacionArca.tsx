import { useCallback, useEffect, useState } from "react";
import {
  arcaApi,
  estadoFiscal,
  type TablaComprobante,
  type ValidacionArca as Validacion,
} from "../api/arca";
import { mensajeDeError } from "../api/client";
import { formatearFechaContable } from "../api/planCuentas";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "./Alerta";

interface Props {
  tabla: TablaComprobante;
  id: number;
  cae: string | null;
  caeVencimiento: string | null;
  estado: string | null;
  anulado: boolean;
  /** Se llama después de validar, para recargar el comprobante (estado fiscal y vencimiento del CAE). */
  onValidado: () => void;
}

const TIPO_ALERTA: Record<string, "exito" | "aviso" | "error"> = {
  VALIDO: "exito",
  OBSERVADO: "aviso",
  PENDIENTE_AUDITORIA: "aviso",
  ERROR_INTEGRACION: "aviso",
  INVALIDO: "error",
};

function formatearFechaHora(valor: string | null): string {
  if (!valor) return "—";
  const fecha = new Date(valor.endsWith("Z") || valor.includes("+") ? valor : `${valor}Z`);
  return fecha.toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" });
}

export function EtiquetaEstadoFiscal({ estado }: { estado: string | null | undefined }) {
  const e = estadoFiscal(estado);
  return <span className={`etiqueta ${e.clase}`}>{e.etiqueta}</span>;
}

/** CUU-017 Validar comprobante con ARCA: estado fiscal, validación y su resultado, e historial de intentos. */
export function ValidacionArca({ tabla, id, cae, caeVencimiento, estado, anulado, onValidado }: Props) {
  const { usuario } = useAuth();
  const puedeValidar = usuario?.nivel_acceso === "CONTADOR" || usuario?.nivel_acceso === "ADMINISTRATIVO";
  const [historial, setHistorial] = useState<Validacion[]>([]);
  const [resultado, setResultado] = useState<Validacion | null>(null);
  const [validando, setValidando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const cargarHistorial = useCallback(() => {
    arcaApi
      .historial(tabla, id)
      .then(setHistorial)
      .catch((err) => setError(mensajeDeError(err)));
  }, [tabla, id]);

  useEffect(cargarHistorial, [cargarHistorial]);

  async function validar() {
    setValidando(true);
    setError(null);
    setResultado(null);
    try {
      setResultado(await arcaApi.validar(tabla, id));
      cargarHistorial();
      onValidado();
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setValidando(false);
    }
  }

  return (
    <>
      <h3 className="subtitulo">Validación con ARCA</h3>
      <dl className="ficha ficha-doble">
        <dt>CAE</dt>
        <dd>{cae ?? "—"}</dd>
        <dt>Vencimiento del CAE</dt>
        <dd>{formatearFechaContable(caeVencimiento)}</dd>
        <dt>Estado fiscal</dt>
        <dd>
          <EtiquetaEstadoFiscal estado={estado} />
        </dd>
      </dl>

      {error && <Alerta tipo="error">{error}</Alerta>}
      {resultado && (
        <Alerta tipo={TIPO_ALERTA[resultado.estado] ?? "aviso"} onCerrar={() => setResultado(null)}>
          {resultado.mensaje}
        </Alerta>
      )}
      {resultado && resultado.diferencias.length > 0 && (
        <div className="tabla-contenedor">
          <table className="tabla tabla-compacta">
            <thead>
              <tr>
                <th>Dato</th>
                <th>Registrado</th>
                <th>Informado por ARCA</th>
              </tr>
            </thead>
            <tbody>
              {resultado.diferencias.map((d) => (
                <tr key={d.campo}>
                  <td>{d.etiqueta}</td>
                  <td>{d.registrado ?? "—"}</td>
                  <td>
                    <strong>{d.arca ?? "—"}</strong>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {puedeValidar && !anulado && (
        <p>
          {cae ? (
            <button type="button" className="boton boton-secundario" onClick={validar} disabled={validando}>
              {validando ? "Consultando a ARCA…" : estado === "PENDIENTE" ? "Validar con ARCA" : "Validar nuevamente"}
            </button>
          ) : (
            <span className="texto-secundario">Para validar el comprobante con ARCA, cargue su CAE.</span>
          )}
        </p>
      )}

      {historial.length > 0 && (
        <div className="tabla-contenedor">
          <table className="tabla tabla-compacta">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Resultado</th>
                <th>Detalle</th>
              </tr>
            </thead>
            <tbody>
              {historial.map((v) => (
                <tr key={v.id_validacion}>
                  <td>{formatearFechaHora(v.fecha_inicio)}</td>
                  <td>{v.usuario ?? "—"}</td>
                  <td>
                    <EtiquetaEstadoFiscal estado={v.estado} />
                  </td>
                  <td>{v.mensaje ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
