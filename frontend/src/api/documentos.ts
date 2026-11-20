import { api, apiArchivo } from "./client";
import type { CondicionPago } from "./compras";
import type { TipoComprobante } from "./ventas";

export type OperacionDocumento = "COMPRA" | "VENTA";
export type EstadoDocumento = "PENDIENTE_REVISION" | "REGISTRADO" | "DESCARTADO";

export const ESTADOS_DOCUMENTO: { valor: EstadoDocumento; etiqueta: string }[] = [
  { valor: "PENDIENTE_REVISION", etiqueta: "Pendiente de revisión" },
  { valor: "REGISTRADO", etiqueta: "Registrado" },
  { valor: "DESCARTADO", etiqueta: "Descartado" },
];

export function etiquetaEstadoDocumento(estado: string | null): string {
  return ESTADOS_DOCUMENTO.find((e) => e.valor === estado)?.etiqueta ?? estado ?? "—";
}

export interface CampoDocumento {
  campo: string;
  etiqueta: string;
  valor_extraido: string | null;
  confianza: string | null;
  requiere_revision: boolean;
  valor_final: string | null;
  corregido: boolean;
  revisado: boolean;
}

export interface ValidacionDocumento {
  codigo: string;
  mensaje: string;
  campos: string[];
  nivel: "error" | "advertencia";
}

export interface ComprobanteAsociado {
  tabla: "COMPRA" | "VENTA";
  id: number;
}

export interface Documento {
  id_documento: number;
  operacion: OperacionDocumento | null;
  estado: EstadoDocumento | null;
  nombre_archivo: string | null;
  tipo_contenido: string | null;
  tamanio_bytes: number | null;
  fecha_carga: string | null;
  fecha_registro: string | null;
  usuario: string | null;
  motor_ocr: string | null;
  confianza_ocr: string | null;
  aviso_ocr: string | null;
  umbral_confianza: number;
  campos: CampoDocumento[];
  validaciones: ValidacionDocumento[];
  contraparte_sugerida: { id: number; codigo: string; cuit: string | null; razon_social: string | null; activo: boolean } | null;
  comprobante: ComprobanteAsociado | null;
}

export interface DocumentoResumen {
  id_documento: number;
  operacion: OperacionDocumento | null;
  estado: EstadoDocumento | null;
  nombre_archivo: string | null;
  fecha_carga: string | null;
  usuario: string | null;
  comprobante: ComprobanteAsociado | null;
  tipo_comprobante: string | null;
  numero: string | null;
  razon_social: string | null;
  importe_total: string | null;
  /** Moneda del total; null en documentos anteriores (pesos). */
  moneda: Moneda | null;
}

export type Moneda = "ARS" | "USD" | "EUR";

export const MONEDAS: { valor: Moneda; etiqueta: string }[] = [
  { valor: "ARS", etiqueta: "Pesos (ARS)" },
  { valor: "USD", etiqueta: "Dólares (USD)" },
  { valor: "EUR", etiqueta: "Euros (EUR)" },
];

/** Importe con el símbolo de su moneda (pesos si no se indica). */
export function formatearEnMoneda(valor: string | number, moneda: string | null | undefined): string {
  const codigo = moneda && MONEDAS.some((m) => m.valor === moneda) ? moneda : "ARS";
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: codigo }).format(Number(valor));
}

/**
 * Importes en pesos, como los convierte el backend al registrar: cada uno por la cotización, redondeado al
 * centavo; si en la moneda original el total es la suma de las partes, el total en pesos es la suma convertida.
 * Recibe y devuelve centavos.
 */
export function convertirAPesos(
  centavos: { neto: number; iva: number; otros: number; total: number },
  cotizacion: number,
): { neto: number; iva: number; otros: number; total: number } {
  const convertir = (c: number) => Math.round(c * cotizacion);
  const neto = convertir(centavos.neto);
  const iva = convertir(centavos.iva);
  const otros = convertir(centavos.otros);
  const cuadra = centavos.neto + centavos.iva + centavos.otros === centavos.total;
  return { neto, iva, otros, total: cuadra ? neto + iva + otros : convertir(centavos.total) };
}

export interface RegistroDocumento {
  id_contraparte: number;
  tipo_comprobante: TipoComprobante;
  punto_venta: number;
  numero_comprobante: number;
  fecha_emision: string;
  fecha_contable: string | null;
  condicion: CondicionPago;
  importe_neto_gravado: string;
  importe_iva: string;
  importe_otros_impuestos: string;
  importe_total: string;
  /** Los importes están en esta moneda; si no es pesos, el backend los convierte con la cotización. */
  moneda: Moneda;
  cotizacion: string | null;
  campos_revisados: string[];
}

export interface FiltrosDocumentos {
  estado?: EstadoDocumento;
  operacion?: OperacionDocumento;
  tabla_asociada?: "COMPRA" | "VENTA";
  id_registro?: number;
}

const URL = "/documentos";

export const documentosApi = {
  listar: (filtros: FiltrosDocumentos = {}) => {
    const params = new URLSearchParams();
    if (filtros.estado) params.set("estado", filtros.estado);
    if (filtros.operacion) params.set("operacion", filtros.operacion);
    if (filtros.tabla_asociada) params.set("tabla_asociada", filtros.tabla_asociada);
    if (filtros.id_registro) params.set("id_registro", String(filtros.id_registro));
    const query = params.toString();
    return api<DocumentoResumen[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  obtener: (id: number) => api<Documento>(`${URL}/${id}`),
  cargar: (archivo: File, operacion: OperacionDocumento) => {
    const formulario = new FormData();
    formulario.append("archivo", archivo);
    formulario.append("operacion", operacion);
    return api<Documento>(URL, { method: "POST", body: formulario });
  },
  archivo: (id: number) => apiArchivo(`${URL}/${id}/archivo`),
  registrar: (id: number, datos: RegistroDocumento) =>
    api<Documento>(`${URL}/${id}/registrar`, { method: "POST", body: datos }),
  descartar: (id: number) => api<Documento>(`${URL}/${id}/descartar`, { method: "POST" }),
};

/** Nivel de confianza para mostrar: alta (≥ umbral), media o baja. */
export function nivelConfianza(confianza: string | null, umbral: number): "alta" | "media" | "baja" {
  const c = Number(confianza ?? 0);
  if (c >= umbral) return "alta";
  return c >= umbral / 2 ? "media" : "baja";
}
