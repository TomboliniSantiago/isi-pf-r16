/** Datos comunes a clientes y proveedores (CUU-007 / CUU-008). */
export const CONDICIONES_IVA = ["Responsable Inscripto", "Monotributo", "Exento", "Consumidor Final"] as const;
export type CondicionIva = (typeof CONDICIONES_IVA)[number];

export interface DatosContribuyente {
  cuit: string;
  razon_social: string;
  condicion_iva: CondicionIva;
  domicilio: string;
  localidad: string;
  provincia: string;
}
