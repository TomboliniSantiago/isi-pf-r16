import { api } from "./client";
import type { CondicionIva, DatosContribuyente } from "./contribuyentes";

export interface ProveedorResumen {
  id_proveedor: number;
  codigo: string;
  cuit: string | null;
  razon_social: string | null;
  activo: boolean;
}

export interface Proveedor extends ProveedorResumen {
  condicion_iva: string | null;
  domicilio: string | null;
  localidad: string | null;
  provincia: string | null;
}

export interface ProveedorDetalle extends Proveedor {
  cantidad_comprobantes: number;
  comprobantes_pendientes: number;
}

export type ProveedorDatos = DatosContribuyente;

export interface ConsultaCuit {
  cuit: string;
  en_padron: boolean;
  datos: Omit<ProveedorDatos, "cuit"> | null;
  proveedor_existente: ProveedorResumen | null;
}

export interface Comprobante {
  id_compra: number;
  tipo_comprobante: string | null;
  numero: string;
  fecha_emision: string | null;
  moneda: string | null;
  importe_total: string | null;
  asentado: boolean;
  pendiente: boolean;
}

export interface FiltrosProveedores {
  buscar?: string;
  condicion_iva?: CondicionIva;
  activo?: boolean;
}

const URL = "/proveedores";

export const proveedoresApi = {
  listar: (filtros: FiltrosProveedores = {}) => {
    const params = new URLSearchParams();
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    if (filtros.condicion_iva) params.set("condicion_iva", filtros.condicion_iva);
    if (filtros.activo !== undefined) params.set("activo", String(filtros.activo));
    const query = params.toString();
    return api<Proveedor[]>(`${URL}${query ? `?${query}` : ""}`);
  },
  consultarCuit: (cuit: string) => api<ConsultaCuit>(`${URL}/consulta-cuit?cuit=${encodeURIComponent(cuit)}`),
  obtener: (id: number) => api<ProveedorDetalle>(`${URL}/${id}`),
  comprobantes: (id: number) => api<Comprobante[]>(`${URL}/${id}/comprobantes`),
  crear: (datos: ProveedorDatos) => api<Proveedor>(URL, { method: "POST", body: datos }),
  modificar: (id: number, datos: ProveedorDatos) => api<Proveedor>(`${URL}/${id}`, { method: "PUT", body: datos }),
  verificarBaja: (id: number) => api<{ valido: boolean; mensaje: string }>(`${URL}/${id}/verificar-baja`),
  darDeBaja: (id: number) => api<Proveedor>(`${URL}/${id}/baja`, { method: "POST" }),
  reactivar: (id: number) => api<Proveedor>(`${URL}/${id}/reactivar`, { method: "POST" }),
};

export function datosDe(proveedor: Proveedor): ProveedorDatos {
  return {
    cuit: proveedor.cuit ?? "",
    razon_social: proveedor.razon_social ?? "",
    condicion_iva: (proveedor.condicion_iva as CondicionIva | null) ?? "Responsable Inscripto",
    domicilio: proveedor.domicilio ?? "",
    localidad: proveedor.localidad ?? "",
    provincia: proveedor.provincia ?? "",
  };
}
