import { api } from "./client";

export type EstadoVenta = "PENDIENTE" | "CONTABILIZADA" | "ANULADA";
export type TipoComprobante = "Factura A" | "Factura B" | "Factura C";
export type CondicionCobro = "Contado" | "Cuenta Corriente" | "Transferencia";

export const ESTADOS_VENTA: { valor: EstadoVenta; etiqueta: string }[] = [
  { valor: "CONTABILIZADA", etiqueta: "Contabilizada" },
  { valor: "PENDIENTE", etiqueta: "Pendiente" },
  { valor: "ANULADA", etiqueta: "Anulada" },
];

export const TIPOS_COMPROBANTE: TipoComprobante[] = ["Factura A", "Factura B", "Factura C"];

/** La condición de cobro define la cuenta del Debe (CUU-001 paso 4). */
export const CONDICIONES_COBRO: { valor: CondicionCobro; cuenta: string }[] = [
  { valor: "Contado", cuenta: "Caja" },
  { valor: "Cuenta Corriente", cuenta: "Deudores por ventas" },
  { valor: "Transferencia", cuenta: "Banco" },
];

export function etiquetaEstadoVenta(estado: string | null): string {
  return ESTADOS_VENTA.find((e) => e.valor === estado)?.etiqueta ?? estado ?? "—";
}

/** Cuentas elegidas por el usuario cuando no hay cuenta predeterminada (4.a). */
export interface CuentasVenta {
  cobro?: number | null;
  ventas?: number | null;
  iva?: number | null;
  otros_impuestos?: number | null;
}

export interface VentaDatos {
  id_cliente: number;
  tipo_comprobante: TipoComprobante;
  punto_venta: number;
  numero_comprobante: number;
  fecha_emision: string;
  fecha_contable: string | null;
  condicion_venta: CondicionCobro;
  importe_neto_gravado: string;
  importe_iva: string;
  importe_otros_impuestos: string;
  importe_total: string;
  cuentas: CuentasVenta;
  confirmar: boolean;
}

export interface Venta {
  id_venta: number;
  cliente: { id_cliente: number; codigo: string; cuit: string | null; razon_social: string | null } | null;
  tipo_comprobante: string | null;
  punto_venta: number | null;
  numero_comprobante: number | null;
  numero: string;
  fecha_emision: string | null;
  fecha_contable: string | null;
  condicion_venta: string | null;
  moneda: string | null;
  importe_neto_gravado: string | null;
  importe_iva: string | null;
  importe_otros_impuestos: string | null;
  importe_total: string | null;
  cae: string | null;
  estado: EstadoVenta | null;
  asiento: { id_asiento: number; numero_asiento: number | null; estado: string | null; revertido_por: number | null } | null;
}

export type RolCuenta = keyof CuentasVenta;

export interface LineaPropuesta {
  rol: RolCuenta;
  descripcion: string;
  id_cuenta: number | null;
  codigo: string | null;
  nombre: string | null;
  debe: string;
  haber: string;
}

export interface Propuesta {
  lineas: LineaPropuesta[];
  total_debe: string;
  total_haber: string;
  diferencia: string;
  balanceado: boolean;
  cuentas_faltantes: string[];
  duplicado: Venta | null;
}

export interface FiltrosVentas {
  desde?: string;
  hasta?: string;
  id_cliente?: number;
  estado?: EstadoVenta;
  buscar?: string;
}

const URL = "/ventas";

export const ventasApi = {
  listar: (filtros: FiltrosVentas = {}) => {
    const params = new URLSearchParams();
    if (filtros.desde) params.set("desde", filtros.desde);
    if (filtros.hasta) params.set("hasta", filtros.hasta);
    if (filtros.id_cliente) params.set("id_cliente", String(filtros.id_cliente));
    if (filtros.estado) params.set("estado", filtros.estado);
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    const query = params.toString();
    return api<Venta[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  obtener: (id: number) => api<Venta>(`${URL}/${id}`),
  proponer: (datos: VentaDatos) => api<Propuesta>(`${URL}/propuesta`, { method: "POST", body: datos }),
  crear: (datos: VentaDatos) => api<Venta>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: VentaDatos) => api<Venta>(`${URL}/${id}`, { method: "PUT", body: datos }),
  contabilizar: (id: number, cuentas: CuentasVenta = {}) =>
    api<Venta>(`${URL}/${id}/contabilizar`, { method: "POST", body: cuentas }),
  anular: (id: number) => api<Venta>(`${URL}/${id}/anular`, { method: "POST" }),
};
