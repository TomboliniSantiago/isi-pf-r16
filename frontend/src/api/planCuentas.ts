import { api } from "./client";

export type TipoCuenta = "ACTIVO" | "PASIVO" | "PATRIMONIO_NETO" | "INGRESOS" | "GASTOS";
export type Naturaleza = "DEUDORA" | "ACREEDORA";

export const TIPOS: { valor: TipoCuenta; etiqueta: string }[] = [
  { valor: "ACTIVO", etiqueta: "Activo" },
  { valor: "PASIVO", etiqueta: "Pasivo" },
  { valor: "PATRIMONIO_NETO", etiqueta: "Patrimonio neto" },
  { valor: "INGRESOS", etiqueta: "Ingresos" },
  { valor: "GASTOS", etiqueta: "Gastos" },
];

export function etiquetaTipo(tipo: string | null): string {
  return TIPOS.find((t) => t.valor === tipo)?.etiqueta ?? tipo ?? "—";
}

export function etiquetaNaturaleza(naturaleza: string | null): string {
  if (naturaleza === "DEUDORA") return "Deudora";
  if (naturaleza === "ACREEDORA") return "Acreedora";
  return "—";
}

export interface CuentaResumen {
  id_cuenta: number;
  codigo: string | null;
  nombre: string | null;
}

export interface Cuenta {
  id_cuenta: number;
  codigo: string | null;
  nombre: string | null;
  tipo_cuenta: TipoCuenta | null;
  naturaleza: Naturaleza | null;
  imputable: boolean;
  activa: boolean;
  id_cuenta_padre: number | null;
  codigo_padre: string | null;
  nivel: number;
}

export interface CuentaDetalle extends Cuenta {
  ruta: CuentaResumen[];
  cantidad_hijas: number;
  cantidad_movimientos: number;
  predeterminada_para: string[];
}

export interface CuentaDatos {
  codigo: string;
  nombre: string;
  tipo_cuenta: TipoCuenta;
  naturaleza: Naturaleza | null;
  imputable: boolean;
  id_cuenta_padre: number | null;
}

export interface Movimiento {
  id_asiento: number;
  numero_asiento: number | null;
  fecha: string | null;
  concepto: string | null;
  estado: string | null;
  debe: string;
  haber: string;
}

export interface Predeterminada {
  clave: string;
  descripcion: string;
  cuenta: CuentaResumen | null;
  /** Regla de coherencia: tipos admitidos y, si no es null, naturaleza exigida. */
  tipos_admitidos: TipoCuenta[];
  naturaleza: Naturaleza | null;
  requisito: string;
}

/** Misma regla que valida el backend; una naturaleza vacía (cuenta heredada) no se considera incoherente. */
export function esCoherente(cuenta: Cuenta, regla: Predeterminada): boolean {
  return (
    cuenta.tipo_cuenta !== null &&
    regla.tipos_admitidos.includes(cuenta.tipo_cuenta) &&
    (regla.naturaleza === null || cuenta.naturaleza === null || cuenta.naturaleza === regla.naturaleza)
  );
}

export interface Validacion {
  valido: boolean;
  mensaje: string;
}

export interface FiltrosCuentas {
  buscar?: string;
  tipo?: TipoCuenta;
  activa?: boolean;
  imputable?: boolean;
}

const URL = "/plan-cuentas";

export const planCuentasApi = {
  listar: (filtros: FiltrosCuentas = {}) => {
    const params = new URLSearchParams();
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    if (filtros.tipo) params.set("tipo", filtros.tipo);
    if (filtros.activa !== undefined) params.set("activa", String(filtros.activa));
    if (filtros.imputable !== undefined) params.set("imputable", String(filtros.imputable));
    const query = params.toString();
    return api<Cuenta[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  obtener: (id: number) => api<CuentaDetalle>(`${URL}/${id}`),
  movimientos: (id: number) => api<Movimiento[]>(`${URL}/${id}/movimientos`),
  validar: (datos: CuentaDatos, idCuenta?: number) =>
    api<Validacion>(`${URL}/validar${idCuenta ? `?id_cuenta=${idCuenta}` : ""}`, { method: "POST", body: datos }),
  crear: (datos: CuentaDatos) => api<Cuenta>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: CuentaDatos) => api<Cuenta>(`${URL}/${id}`, { method: "PUT", body: datos }),
  verificarBaja: (id: number) => api<Validacion>(`${URL}/${id}/verificar-baja`),
  darDeBaja: (id: number) => api<Cuenta>(`${URL}/${id}/baja`, { method: "POST" }),
  reactivar: (id: number) => api<Cuenta>(`${URL}/${id}/reactivar`, { method: "POST" }),
  predeterminadas: () => api<Predeterminada[]>(`${URL}/predeterminadas`),
  asignarPredeterminada: (clave: string, idCuenta: number | null) =>
    api<Predeterminada>(`${URL}/predeterminadas/${clave}`, { method: "PUT", body: { id_cuenta: idCuenta } }),
};

export function formatearImporte(valor: string | number): string {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" }).format(Number(valor));
}

/** Fecha "AAAA-MM-DD" a "DD/MM/AAAA" sin pasar por Date (evita el corrimiento por zona horaria). */
export function formatearFechaContable(fecha: string | null): string {
  if (!fecha) return "—";
  const [anio, mes, dia] = fecha.split("-");
  return `${dia}/${mes}/${anio}`;
}
