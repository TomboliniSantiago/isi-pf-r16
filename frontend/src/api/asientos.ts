import { api } from "./client";

export type EstadoAsiento = "BORRADOR" | "ASENTADO" | "ANULADO";
export type OrigenAsiento = "MANUAL" | "VENTA" | "COMPRA" | "REVERSION";

export const ESTADOS: { valor: EstadoAsiento; etiqueta: string }[] = [
  { valor: "ASENTADO", etiqueta: "Vigente" },
  { valor: "BORRADOR", etiqueta: "Pendiente" },
  { valor: "ANULADO", etiqueta: "Anulado" },
];

export const ORIGENES: { valor: OrigenAsiento; etiqueta: string }[] = [
  { valor: "MANUAL", etiqueta: "Manual" },
  { valor: "VENTA", etiqueta: "Venta" },
  { valor: "COMPRA", etiqueta: "Compra" },
  { valor: "REVERSION", etiqueta: "Reversión" },
];

export function etiquetaEstado(estado: string | null): string {
  return ESTADOS.find((e) => e.valor === estado)?.etiqueta ?? estado ?? "—";
}

export function etiquetaOrigen(origen: string | null): string {
  return ORIGENES.find((o) => o.valor === origen)?.etiqueta ?? origen ?? "—";
}

export interface Linea {
  id_detalle_asiento: number;
  id_cuenta: number;
  codigo: string | null;
  nombre: string | null;
  debe: string;
  haber: string;
}

export interface Asiento {
  id_asiento: number;
  numero_asiento: number | null;
  fecha: string | null;
  concepto: string | null;
  referencia: string | null;
  tipo_origen: OrigenAsiento | null;
  estado: EstadoAsiento | null;
  id_venta: number | null;
  id_compra: number | null;
  revierte_a: number | null;
  revertido_por: number | null;
  total_debe: string;
  total_haber: string;
  lineas: Linea[];
}

export interface LineaDatos {
  id_cuenta: number;
  debe: string;
  haber: string;
}

export interface AsientoDatos {
  fecha: string;
  concepto: string;
  referencia: string | null;
  lineas: LineaDatos[];
  confirmar: boolean;
}

export interface Totales {
  total_debe: string;
  total_haber: string;
  diferencia: string;
  balanceado: boolean;
}

export interface FiltrosDiario {
  desde?: string;
  hasta?: string;
  id_cuenta?: number;
  tipo_origen?: OrigenAsiento;
  estado?: EstadoAsiento;
}

const URL = "/asientos";

export const asientosApi = {
  listar: (filtros: FiltrosDiario = {}) => {
    const params = new URLSearchParams();
    if (filtros.desde) params.set("desde", filtros.desde);
    if (filtros.hasta) params.set("hasta", filtros.hasta);
    if (filtros.id_cuenta) params.set("id_cuenta", String(filtros.id_cuenta));
    if (filtros.tipo_origen) params.set("tipo_origen", filtros.tipo_origen);
    if (filtros.estado) params.set("estado", filtros.estado);
    const query = params.toString();
    return api<Asiento[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  obtener: (id: number) => api<Asiento>(`${URL}/${id}`),
  totales: (lineas: LineaDatos[]) => api<Totales>(`${URL}/totales`, { method: "POST", body: lineas }),
  crear: (datos: AsientoDatos) => api<Asiento>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: AsientoDatos) => api<Asiento>(`${URL}/${id}`, { method: "PUT", body: datos }),
  confirmar: (id: number) => api<Asiento>(`${URL}/${id}/confirmar`, { method: "POST" }),
  anular: (id: number) => api<Asiento>(`${URL}/${id}/anular`, { method: "POST" }),
};

/** Un asiento manual vigente o pendiente puede modificarse o anularse desde el Libro Diario. */
export function esGestionable(asiento: Asiento): boolean {
  return asiento.tipo_origen === "MANUAL" && asiento.estado !== "ANULADO";
}
