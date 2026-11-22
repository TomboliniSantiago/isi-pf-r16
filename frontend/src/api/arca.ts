import { api } from "./client";

/** CUU-017: estado de la validación con ARCA de una venta o compra (independiente del estado contable). */
export type EstadoFiscal =
  | "PENDIENTE"
  | "EN_VALIDACION"
  | "VALIDO"
  | "INVALIDO"
  | "OBSERVADO"
  | "PENDIENTE_AUDITORIA"
  | "ERROR_INTEGRACION";

export const ESTADOS_FISCALES: { valor: EstadoFiscal; etiqueta: string; clase: string }[] = [
  { valor: "PENDIENTE", etiqueta: "Pendiente de validación", clase: "etiqueta-neutra" },
  { valor: "EN_VALIDACION", etiqueta: "En validación", clase: "etiqueta-pendiente" },
  { valor: "VALIDO", etiqueta: "Válido", clase: "etiqueta-activo" },
  { valor: "INVALIDO", etiqueta: "No válido", clase: "etiqueta-baja" },
  { valor: "OBSERVADO", etiqueta: "Observado", clase: "etiqueta-alerta" },
  { valor: "PENDIENTE_AUDITORIA", etiqueta: "Pendiente de auditoría", clase: "etiqueta-alerta" },
  { valor: "ERROR_INTEGRACION", etiqueta: "Error de integración", clase: "etiqueta-baja" },
];

export function estadoFiscal(valor: string | null | undefined) {
  return (
    ESTADOS_FISCALES.find((e) => e.valor === valor) ?? { valor, etiqueta: valor ?? "—", clase: "etiqueta-neutra" }
  );
}

export interface DiferenciaArca {
  campo: string;
  etiqueta: string;
  registrado: string | null;
  arca: string | null;
}

export interface ValidacionArca {
  id_validacion: number;
  fecha_inicio: string;
  fecha_respuesta: string | null;
  usuario: string | null;
  estado: EstadoFiscal;
  mensaje: string | null;
  diferencias: DiferenciaArca[];
  cae_vencimiento_arca: string | null;
}

export type TablaComprobante = "COMPRA" | "VENTA";

const URL: Record<TablaComprobante, string> = { COMPRA: "/compras", VENTA: "/ventas" };

export const arcaApi = {
  validar: (tabla: TablaComprobante, id: number) =>
    api<ValidacionArca>(`${URL[tabla]}/${id}/validar-arca`, { method: "POST" }),
  historial: (tabla: TablaComprobante, id: number) => api<ValidacionArca[]>(`${URL[tabla]}/${id}/validaciones`),
};

/** CAE de ARCA: 14 dígitos. */
export function caeValido(cae: string): boolean {
  return /^\d{14}$/.test(cae);
}
