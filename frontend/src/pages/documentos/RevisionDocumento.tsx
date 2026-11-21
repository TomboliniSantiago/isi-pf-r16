import { useState } from "react";
import { caeValido } from "../../api/arca";
import { mensajeDeError } from "../../api/client";
import type { Cliente } from "../../api/clientes";
import { CONDICIONES_PAGO, type CondicionPago } from "../../api/compras";
import {
  MONEDAS,
  convertirAPesos,
  documentosApi,
  formatearEnMoneda,
  nivelConfianza,
  type CampoDocumento,
  type Documento,
  type Moneda,
  type RegistroDocumento,
} from "../../api/documentos";
import { formatearImporte } from "../../api/planCuentas";
import type { Proveedor } from "../../api/proveedores";
import { TIPOS_COMPROBANTE, type TipoComprobante } from "../../api/ventas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { AltaCliente } from "../clientes/AltaCliente";
import { AltaProveedor } from "../proveedores/AltaProveedor";
import { VistaArchivo } from "./VistaArchivo";

interface Props {
  documento: Documento;
  /** Proveedores (compra) o clientes (venta) vigentes. */
  contrapartes: (Proveedor | Cliente)[];
  onCerrar: () => void;
  onRegistrado: (documento: Documento) => void;
  onDescartado: (mensaje: string) => void;
  onContraparteCreada: (contraparte: Proveedor | Cliente) => void;
}

const EDITABLES = [
  "tipo_comprobante",
  "punto_venta",
  "numero_comprobante",
  "fecha_emision",
  "importe_neto_gravado",
  "importe_iva",
  "importe_otros_impuestos",
  "importe_total",
  "moneda",
  "cotizacion",
  "cae",
  "cae_vencimiento",
] as const;
const IMPORTES = new Set(["importe_neto_gravado", "importe_iva", "importe_otros_impuestos", "importe_total"]);
// Documentos cargados antes de reconocer la moneda: no tienen esos campos y se asumen en pesos.
const POR_DEFECTO: Record<string, string> = { moneda: "ARS", cotizacion: "1" };

const idDe = (c: Proveedor | Cliente) => ("id_proveedor" in c ? c.id_proveedor : c.id_cliente);

function aCentavos(valor: string): number {
  const n = Number((valor || "0").replace(",", "."));
  return Number.isFinite(n) ? Math.round(n * 100) : NaN;
}

/**
 * CUU-016 pasos 5-8: el usuario revisa los datos extraídos junto al archivo original, con su nivel de
 * confianza y las validaciones; corrige lo necesario, revisa los campos marcados (4.a / 6.a) y registra.
 */
export function RevisionDocumento({ documento, contrapartes, onCerrar, onRegistrado, onDescartado, onContraparteCreada }: Props) {
  const esCompra = documento.operacion === "COMPRA";
  const campos = Object.fromEntries(documento.campos.map((c) => [c.campo, c])) as Record<string, CampoDocumento>;
  const [valores, setValores] = useState<Record<string, string>>(() => ({
    ...POR_DEFECTO,
    ...Object.fromEntries(documento.campos.map((c) => [c.campo, c.valor_extraido ?? POR_DEFECTO[c.campo] ?? ""])),
  }));
  const [revisados, setRevisados] = useState<Set<string>>(new Set());
  const sugerida = documento.contraparte_sugerida;
  const [idContraparte, setIdContraparte] = useState(sugerida?.activo ? String(sugerida.id) : "");
  const [condicion, setCondicion] = useState<CondicionPago>("Cuenta Corriente");
  const [fechaContable, setFechaContable] = useState("");
  const [altaContraparte, setAltaContraparte] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const aRevisar = documento.campos.filter((c) => c.requiere_revision).map((c) => c.campo);
  const pendientes = aRevisar.filter((c) => !revisados.has(c));
  const suma = ["importe_neto_gravado", "importe_iva", "importe_otros_impuestos"].reduce((s, c) => s + aCentavos(valores[c]), 0);
  const diferencia = aCentavos(valores.importe_total) - suma;
  const nombre = esCompra ? "proveedor" : "cliente";
  const moneda = (valores.moneda || "ARS") as Moneda;
  const extranjera = moneda !== "ARS";
  const cotizacion = Number((valores.cotizacion || "").replace(",", "."));
  const cotizacionValida = Number.isFinite(cotizacion) && cotizacion > 0;
  const enPesos =
    extranjera && cotizacionValida
      ? convertirAPesos(
          {
            neto: aCentavos(valores.importe_neto_gravado),
            iva: aCentavos(valores.importe_iva),
            otros: aCentavos(valores.importe_otros_impuestos),
            total: aCentavos(valores.importe_total),
          },
          cotizacion,
        )
      : null;

  function cambiar(campo: string, valor: string) {
    setValores((prev) => ({ ...prev, [campo]: valor }));
  }

  function alternarRevisado(campo: string) {
    setRevisados((prev) => {
      const nuevo = new Set(prev);
      if (nuevo.has(campo)) nuevo.delete(campo);
      else nuevo.add(campo);
      return nuevo;
    });
  }

  function validarFormulario(): string | null {
    if (!idContraparte) return `Seleccione el ${nombre} del comprobante.`;
    if (!TIPOS_COMPROBANTE.includes(valores.tipo_comprobante as TipoComprobante)) return "Seleccione el tipo de comprobante.";
    if (!(Number(valores.punto_venta) >= 1)) return "Indique el punto de venta.";
    if (!(Number(valores.numero_comprobante) >= 1)) return "Indique el número de comprobante.";
    if (!valores.fecha_emision) return "Indique la fecha de emisión.";
    for (const c of IMPORTES) {
      const centavos = aCentavos(valores[c]);
      if (Number.isNaN(centavos) || centavos < 0) return `El importe de ${campos[c]?.etiqueta ?? c} no es válido.`;
    }
    if (extranjera && !cotizacionValida) return "Indique la cotización para convertir los importes a pesos.";
    if (valores.cae && !caeValido(valores.cae)) return "El CAE debe tener 14 dígitos.";
    if (pendientes.length) return `Revise los campos marcados: ${pendientes.map((c) => campos[c]?.etiqueta ?? c).join(", ")}.`;
    return null;
  }

  async function registrar() {
    const problema = validarFormulario();
    if (problema) {
      setError(problema);
      return;
    }
    const importe = (v: string) => (v ? v.replace(",", ".") : "0");
    const datos: RegistroDocumento = {
      id_contraparte: Number(idContraparte),
      tipo_comprobante: valores.tipo_comprobante as TipoComprobante,
      punto_venta: Number(valores.punto_venta),
      numero_comprobante: Number(valores.numero_comprobante),
      fecha_emision: valores.fecha_emision,
      fecha_contable: fechaContable || null,
      condicion,
      importe_neto_gravado: importe(valores.importe_neto_gravado),
      importe_iva: importe(valores.importe_iva),
      importe_otros_impuestos: importe(valores.importe_otros_impuestos),
      importe_total: importe(valores.importe_total),
      moneda,
      cotizacion: extranjera ? String(cotizacion) : null,
      cae: valores.cae || null,
      cae_vencimiento: valores.cae_vencimiento || null,
      campos_revisados: [...revisados],
    };
    setError(null);
    setEnviando(true);
    try {
      onRegistrado(await documentosApi.registrar(documento.id_documento, datos));
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  async function descartar() {
    setEnviando(true);
    try {
      await documentosApi.descartar(documento.id_documento);
      onDescartado(`El documento ${documento.nombre_archivo} fue descartado.`);
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  if (altaContraparte) {
    const alCrear = (_: string, creado: Proveedor | Cliente) => {
      onContraparteCreada(creado);
      setIdContraparte(String(idDe(creado)));
      setAltaContraparte(false);
    };
    const alVerExistente = (c: { activo: boolean } & ({ id_proveedor: number } | { id_cliente: number })) => {
      if (c.activo) setIdContraparte(String("id_proveedor" in c ? c.id_proveedor : c.id_cliente));
      setAltaContraparte(false);
    };
    return esCompra ? (
      <AltaProveedor onCerrar={() => setAltaContraparte(false)} onCreado={alCrear} onVerExistente={alVerExistente} />
    ) : (
      <AltaCliente onCerrar={() => setAltaContraparte(false)} onCreado={alCrear} onVerExistente={alVerExistente} />
    );
  }

  function Confianza({ campo }: { campo: CampoDocumento }) {
    const nivel = nivelConfianza(campo.confianza, documento.umbral_confianza);
    const porcentaje = Math.round(Number(campo.confianza ?? 0) * 100);
    return (
      <span className={`confianza confianza-${nivel}`} title={`Confianza de la extracción: ${porcentaje}%`}>
        {campo.valor_extraido === null ? "No reconocido" : `${porcentaje}%`}
      </span>
    );
  }

  function Revisar({ campo }: { campo: string }) {
    if (!campos[campo]?.requiere_revision) return null;
    return (
      <label className="revisar-campo">
        <input type="checkbox" checked={revisados.has(campo)} onChange={() => alternarRevisado(campo)} /> Revisado
      </label>
    );
  }

  function entrada(campo: (typeof EDITABLES)[number]) {
    if (campo === "tipo_comprobante") {
      return (
        <select value={valores[campo]} onChange={(e) => cambiar(campo, e.target.value)}>
          <option value="">— Seleccione —</option>
          {TIPOS_COMPROBANTE.map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
      );
    }
    if (campo === "fecha_emision" || campo === "cae_vencimiento") {
      return <input type="date" value={valores[campo] ?? ""} onChange={(e) => cambiar(campo, e.target.value)} />;
    }
    if (campo === "cae") {
      return (
        <input
          inputMode="numeric"
          value={valores[campo] ?? ""}
          onChange={(e) => cambiar(campo, e.target.value.replace(/D/g, ""))}
          maxLength={14}
          placeholder="14 dígitos"
        />
      );
    }
    if (campo === "moneda") {
      return (
        <select value={moneda} onChange={(e) => cambiar(campo, e.target.value)}>
          {MONEDAS.map((m) => (
            <option key={m.valor} value={m.valor}>
              {m.etiqueta}
            </option>
          ))}
        </select>
      );
    }
    if (campo === "cotizacion") {
      return (
        <input
          inputMode="decimal"
          value={extranjera ? valores[campo] : "1"}
          disabled={!extranjera}
          onChange={(e) => cambiar(campo, e.target.value)}
          placeholder="Pesos por unidad"
        />
      );
    }
    const numerico = campo === "punto_venta" || campo === "numero_comprobante";
    return (
      <input
        inputMode={numerico ? "numeric" : "decimal"}
        value={valores[campo]}
        onChange={(e) => cambiar(campo, numerico ? e.target.value.replace(/\D/g, "") : e.target.value)}
        placeholder={numerico ? "" : "0,00"}
      />
    );
  }

  return (
    <Modal
      titulo={`Revisar comprobante de ${esCompra ? "compra" : "venta"}: ${documento.nombre_archivo ?? ""}`}
      onCerrar={onCerrar}
      ancho
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar} disabled={enviando}>
            Revisar más tarde
          </button>
          <button type="button" className="boton boton-peligro" onClick={descartar} disabled={enviando}>
            Descartar
          </button>
          <button type="button" className="boton boton-primario" onClick={registrar} disabled={enviando}>
            {enviando ? "Registrando…" : `Registrar ${esCompra ? "compra" : "venta"}`}
          </button>
        </>
      }
    >
      <div className="revision-documento">
        <VistaArchivo
          idDocumento={documento.id_documento}
          tipoContenido={documento.tipo_contenido}
          nombre={documento.nombre_archivo}
        />
        <div>
          {error && <Alerta tipo="error">{error}</Alerta>}
          {documento.aviso_ocr && <Alerta tipo="aviso">{documento.aviso_ocr}</Alerta>}
          {aRevisar.length > 0 && (
            <Alerta tipo="aviso">
              Hay {aRevisar.length} campo(s) con confianza baja o con inconsistencias: revíselos, corríjalos si hace falta y
              márquelos como revisados antes de registrar.
            </Alerta>
          )}
          {documento.validaciones.map((v) => (
            <Alerta key={v.codigo} tipo={v.nivel === "error" ? "error" : "aviso"}>
              {v.mensaje}
            </Alerta>
          ))}

          <h3 className="subtitulo">{esCompra ? "Proveedor" : "Cliente"}</h3>
          <table className="tabla tabla-compacta tabla-revision">
            <tbody>
              {(["cuit", "razon_social"] as const).map((c) => (
                <tr key={c} className={campos[c]?.requiere_revision ? "fila-revisar" : undefined}>
                  <th>{campos[c]?.etiqueta}</th>
                  <td>{campos[c]?.valor_extraido ?? "—"}</td>
                  <td>{campos[c] && <Confianza campo={campos[c]} />}</td>
                  <td>
                    <Revisar campo={c} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <label className="campo">
            <span>{esCompra ? "Proveedor registrado" : "Cliente registrado"}</span>
            <select value={idContraparte} onChange={(e) => setIdContraparte(e.target.value)}>
              <option value="">— Seleccione el {nombre} —</option>
              {contrapartes.map((c) => (
                <option key={idDe(c)} value={idDe(c)}>
                  {c.razon_social} · {c.cuit}
                </option>
              ))}
            </select>
          </label>
          <p className="texto-secundario">
            {sugerida
              ? sugerida.activo
                ? `Identificado por el CUIT: ${sugerida.razon_social}.`
                : `El ${nombre} con ese CUIT (${sugerida.razon_social}) está dado de baja.`
              : `No se identificó un ${nombre} registrado con el CUIT extraído.`}{" "}
            <button type="button" className="boton-enlace" onClick={() => setAltaContraparte(true)}>
              Registrar {nombre} nuevo
            </button>
          </p>

          <h3 className="subtitulo">Comprobante</h3>
          <table className="tabla tabla-compacta tabla-revision">
            <thead>
              <tr>
                <th>Campo</th>
                <th>Valor</th>
                <th>Confianza</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {EDITABLES.map((c) => {
                const campo = campos[c];
                const modificado = campo && (valores[c] ?? "") !== (campo.valor_extraido ?? "");
                return (
                  <tr key={c} className={campo?.requiere_revision ? "fila-revisar" : undefined}>
                    <th>{campo?.etiqueta ?? c}</th>
                    <td>
                      {entrada(c)}
                      {modificado && (
                        <small className="texto-secundario valor-extraido">Extraído: {campo.valor_extraido ?? "—"}</small>
                      )}
                    </td>
                    <td>{campo && <Confianza campo={campo} />}</td>
                    <td>
                      <Revisar campo={c} />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className={valores.importe_total && diferencia === 0 ? "balance balance-ok" : "balance balance-error"}>
            {diferencia === 0
              ? "El total coincide con neto + IVA + otros impuestos."
              : `El total no coincide con neto + IVA + otros impuestos: diferencia de ${formatearEnMoneda(
                  Math.abs(Number.isNaN(diferencia) ? 0 : diferencia) / 100,
                  moneda,
                )}.`}
          </p>
          {extranjera && (
            <p className="texto-secundario">
              {enPesos
                ? `Se registra en pesos con la cotización: neto ${formatearImporte(enPesos.neto / 100)}, IVA ${formatearImporte(
                    enPesos.iva / 100,
                  )}, otros ${formatearImporte(enPesos.otros / 100)}, total ${formatearImporte(enPesos.total / 100)}.`
                : "Indique la cotización para ver los importes en pesos."}{" "}
              El documento conserva los importes en {moneda}.
            </p>
          )}

          <div className="campos-fila">
            <label className="campo">
              <span>Condición de {esCompra ? "pago" : "cobro"}</span>
              <select value={condicion} onChange={(e) => setCondicion(e.target.value as CondicionPago)}>
                {CONDICIONES_PAGO.map((c) => (
                  <option key={c.valor} value={c.valor}>
                    {c.valor}
                  </option>
                ))}
              </select>
            </label>
            <label className="campo">
              <span>Fecha contable (opcional)</span>
              <input type="date" value={fechaContable} min={valores.fecha_emision} onChange={(e) => setFechaContable(e.target.value)} />
            </label>
          </div>
          <p className="texto-secundario">
            Al registrar se crea la {esCompra ? "compra" : "venta"} como pendiente: después se revisa su asiento y se contabiliza.
            Se conservan el valor extraído y el corregido de cada campo.
          </p>
        </div>
      </div>
    </Modal>
  );
}
