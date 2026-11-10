import { api } from "./client";

export type EstadoCompra = "PENDIENTE" | "CONTABILIZADA" | "ANULADA";
export type TipoComprobante = "Factura A" | "Factura B" | "Factura C";
export type CondicionPago = "Contado" | "Cuenta Corriente" | "Transferencia";

export const ESTADOS_COMPRA: { valor: EstadoCompra; etiqueta: string }[] = [
  { valor: "CONTABILIZADA", etiqueta: "Contabilizada" },
  { valor: "PENDIENTE", etiqueta: "Pendiente" },
  { valor: "ANULADA", etiqueta: "Anulada" },
];

export const TIPOS_COMPROBANTE: TipoComprobante[] = ["Factura A", "Factura B", "Factura C"];

/** La condición de pago define la cuenta del Haber (CUU-002 paso 4). */
export const CONDICIONES_PAGO: { valor: CondicionPago; cuenta: string }[] = [
  { valor: "Contado", cuenta: "Caja" },
  { valor: "Cuenta Corriente", cuenta: "Proveedores" },
  { valor: "Transferencia", cuenta: "Banco" },
];

export function etiquetaEstadoCompra(estado: string | null): string {
  return ESTADOS_COMPRA.find((e) => e.valor === estado)?.etiqueta ?? estado ?? "—";
}

/** Cuentas elegidas por el usuario cuando no hay cuenta predeterminada (4.a). */
export interface CuentasCompra {
  pago?: number | null;
  compras?: number | null;
  iva?: number | null;
  otros_impuestos?: number | null;
}

export interface CompraDatos {
  id_proveedor: number;
  tipo_comprobante: TipoComprobante;
  punto_venta: number;
  numero_comprobante: number;
  fecha_emision: string;
  fecha_contable: string | null;
  condicion_compra: CondicionPago;
  importe_neto_gravado: string;
  importe_iva: string;
  importe_otros_impuestos: string;
  importe_total: string;
  cuentas: CuentasCompra;
  confirmar: boolean;
}

export interface Compra {
  id_compra: number;
  proveedor: { id_proveedor: number; codigo: string; cuit: string | null; razon_social: string | null } | null;
  tipo_comprobante: string | null;
  punto_venta: number | null;
  numero_comprobante: number | null;
  numero: string;
  fecha_emision: string | null;
  fecha_contable: string | null;
  condicion_compra: string | null;
  moneda: string | null;
  importe_neto_gravado: string | null;
  importe_iva: string | null;
  importe_otros_impuestos: string | null;
  importe_total: string | null;
  estado: EstadoCompra | null;
  asiento: { id_asiento: number; numero_asiento: number | null; estado: string | null; revertido_por: number | null } | null;
}

export type RolCuenta = keyof CuentasCompra;

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
  duplicado: Compra | null;
}

export interface FiltrosCompras {
  desde?: string;
  hasta?: string;
  id_proveedor?: number;
  estado?: EstadoCompra;
  buscar?: string;
}

const URL = "/compras";

export const comprasApi = {
  listar: (filtros: FiltrosCompras = {}) => {
    const params = new URLSearchParams();
    if (filtros.desde) params.set("desde", filtros.desde);
    if (filtros.hasta) params.set("hasta", filtros.hasta);
    if (filtros.id_proveedor) params.set("id_proveedor", String(filtros.id_proveedor));
    if (filtros.estado) params.set("estado", filtros.estado);
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    const query = params.toString();
    return api<Compra[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  obtener: (id: number) => api<Compra>(`${URL}/${id}`),
  proponer: (datos: CompraDatos) => api<Propuesta>(`${URL}/propuesta`, { method: "POST", body: datos }),
  crear: (datos: CompraDatos) => api<Compra>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: CompraDatos) => api<Compra>(`${URL}/${id}`, { method: "PUT", body: datos }),
  contabilizar: (id: number, cuentas: CuentasCompra = {}) =>
    api<Compra>(`${URL}/${id}/contabilizar`, { method: "POST", body: cuentas }),
  anular: (id: number) => api<Compra>(`${URL}/${id}/anular`, { method: "POST" }),
};
