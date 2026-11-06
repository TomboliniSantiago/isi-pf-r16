import { api } from "./client";

export const CONDICIONES_IVA = ["Responsable Inscripto", "Monotributo", "Exento", "Consumidor Final"] as const;
export type CondicionIva = (typeof CONDICIONES_IVA)[number];

export interface ClienteResumen {
  id_cliente: number;
  codigo: string;
  cuit: string | null;
  razon_social: string | null;
  activo: boolean;
}

export interface Cliente extends ClienteResumen {
  condicion_iva: string | null;
  domicilio: string | null;
  localidad: string | null;
  provincia: string | null;
}

export interface ClienteDetalle extends Cliente {
  cantidad_comprobantes: number;
  comprobantes_pendientes: number;
}

export interface ClienteDatos {
  cuit: string;
  razon_social: string;
  condicion_iva: CondicionIva;
  domicilio: string;
  localidad: string;
  provincia: string;
}

export interface ConsultaCuit {
  cuit: string;
  en_padron: boolean;
  datos: Omit<ClienteDatos, "cuit"> | null;
  cliente_existente: ClienteResumen | null;
}

export interface Comprobante {
  id_venta: number;
  tipo_comprobante: string | null;
  numero: string;
  fecha_emision: string | null;
  moneda: string | null;
  importe_total: string | null;
  cae: string | null;
  asentado: boolean;
  pendiente: boolean;
}

export interface FiltrosClientes {
  buscar?: string;
  condicion_iva?: CondicionIva;
  activo?: boolean;
}

const URL = "/clientes";

export const clientesApi = {
  listar: (filtros: FiltrosClientes = {}) => {
    const params = new URLSearchParams();
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    if (filtros.condicion_iva) params.set("condicion_iva", filtros.condicion_iva);
    if (filtros.activo !== undefined) params.set("activo", String(filtros.activo));
    const query = params.toString();
    return api<Cliente[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  consultarCuit: (cuit: string) => api<ConsultaCuit>(`${URL}/consulta-cuit?cuit=${encodeURIComponent(cuit)}`),
  obtener: (id: number) => api<ClienteDetalle>(`${URL}/${id}`),
  comprobantes: (id: number) => api<Comprobante[]>(`${URL}/${id}/comprobantes`),
  crear: (datos: ClienteDatos) => api<Cliente>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: ClienteDatos) => api<Cliente>(`${URL}/${id}`, { method: "PUT", body: datos }),
  verificarBaja: (id: number) => api<{ valido: boolean; mensaje: string }>(`${URL}/${id}/verificar-baja`),
  darDeBaja: (id: number) => api<Cliente>(`${URL}/${id}/baja`, { method: "POST" }),
  reactivar: (id: number) => api<Cliente>(`${URL}/${id}/reactivar`, { method: "POST" }),
};

export function datosDe(cliente: Cliente): ClienteDatos {
  return {
    cuit: cliente.cuit ?? "",
    razon_social: cliente.razon_social ?? "",
    condicion_iva: (cliente.condicion_iva as CondicionIva | null) ?? "Responsable Inscripto",
    domicilio: cliente.domicilio ?? "",
    localidad: cliente.localidad ?? "",
    provincia: cliente.provincia ?? "",
  };
}
