export type Rol = "ADMINISTRADOR" | "CONTADOR" | "ADMINISTRATIVO" | "CONSULTA";

export const ROLES: { valor: Rol; etiqueta: string }[] = [
  { valor: "ADMINISTRADOR", etiqueta: "Administrador" },
  { valor: "CONTADOR", etiqueta: "Contador" },
  { valor: "ADMINISTRATIVO", etiqueta: "Administrativo" },
  { valor: "CONSULTA", etiqueta: "Consulta" },
];

export function etiquetaRol(rol: string | null): string {
  return ROLES.find((r) => r.valor === rol)?.etiqueta ?? rol ?? "—";
}

export interface Usuario {
  id_usuario: number;
  nombre_usuario: string | null;
  email: string | null;
  nivel_acceso: string | null;
  activo: boolean;
  bloqueado: boolean;
  debe_cambiar_password: boolean;
  fecha_alta: string | null;
  ultimo_acceso: string | null;
}

export interface UsuarioDatos {
  nombre_usuario: string;
  email: string;
  nivel_acceso: Rol;
}

/** Código de verificación enviado por correo; `desafio` se devuelve junto con el código. */
export interface Desafio {
  desafio: string;
  destino: string;
  expira_en: number;
  reenvio_en: number;
}

export interface LoginRespuesta {
  access_token: string;
  token_type: string;
  expira_en: number;
  usuario: Usuario;
}

export interface UsuarioConPassword {
  usuario: Usuario;
  password_temporal: string;
}

export function formatearFecha(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" });
}
