import { api } from "./client";
import { formatearImporte } from "./planCuentas";

export interface MovimientoMayor {
  fecha: string | null;
  id_asiento: number;
  numero_asiento: number | null;
  tipo_origen: string | null;
  estado: string | null;
  concepto: string | null;
  referencia: string | null;
  id_venta: number | null;
  id_compra: number | null;
  debe: string;
  haber: string;
  saldo: string;
}

export interface CuentaMayor {
  id_cuenta: number;
  codigo: string | null;
  nombre: string | null;
  tipo_cuenta: string | null;
  naturaleza: string | null;
  activa: boolean;
  saldo_inicial: string;
  total_debe: string;
  total_haber: string;
  saldo_final: string;
  movimientos: MovimientoMayor[];
}

export interface LibroMayor {
  id_cuenta: number;
  codigo: string | null;
  nombre: string | null;
  imputable: boolean;
  desde: string | null;
  hasta: string | null;
  cuentas: CuentaMayor[];
  saldo_inicial: string;
  total_debe: string;
  total_haber: string;
  saldo_final: string;
}

export const libroMayorApi = {
  consultar: (idCuenta: number, desde?: string, hasta?: string) => {
    const params = new URLSearchParams({ id_cuenta: String(idCuenta) });
    if (desde) params.set("desde", desde);
    if (hasta) params.set("hasta", hasta);
    return api<LibroMayor>(`/libro-mayor?${params.toString()}`);
  },
};

/** Saldo positivo: deudor (D); negativo: acreedor (A). */
export function formatearSaldo(valor: string | number): string {
  const n = Number(valor);
  if (n === 0) return formatearImporte(0);
  return `${formatearImporte(Math.abs(n))} ${n > 0 ? "D" : "A"}`;
}
