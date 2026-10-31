import type { Rol, Usuario, UsuarioConPassword, UsuarioDatos } from "../types";
import { api } from "./client";

export interface FiltrosUsuarios {
  buscar?: string;
  activo?: boolean;
  rol?: Rol;
}

/** Operaciones que usa la pantalla de gestión de usuarios. */
export interface GestionUsuariosApi {
  listar: (filtros: FiltrosUsuarios) => Promise<Usuario[]>;
  crear: (datos: UsuarioDatos) => Promise<UsuarioConPassword>;
  modificar: (id: number, datos: UsuarioDatos) => Promise<Usuario>;
  darDeBaja: (id: number) => Promise<Usuario>;
  reactivar: (id: number) => Promise<Usuario>;
  /** No disponible sin inicio de sesión. */
  restablecerPassword?: (id: number) => Promise<UsuarioConPassword>;
}

function consulta(filtros: FiltrosUsuarios): string {
  const params = new URLSearchParams();
  if (filtros.buscar) params.set("buscar", filtros.buscar);
  if (filtros.activo !== undefined) params.set("activo", String(filtros.activo));
  if (filtros.rol) params.set("rol", filtros.rol);
  const query = params.toString();
  return query ? `?${query}` : "";
}

export const usuariosApi: GestionUsuariosApi = {
  listar: (filtros) => api<Usuario[]>(`/usuarios${consulta(filtros)}`),
  crear: (datos) => api<UsuarioConPassword>("/usuarios", { method: "POST", body: datos }),
  modificar: (id, datos) => api<Usuario>(`/usuarios/${id}`, { method: "PUT", body: datos }),
  darDeBaja: (id) => api<Usuario>(`/usuarios/${id}/baja`, { method: "POST" }),
  reactivar: (id) => api<Usuario>(`/usuarios/${id}/reactivar`, { method: "POST" }),
  restablecerPassword: (id) => api<UsuarioConPassword>(`/usuarios/${id}/restablecer-password`, { method: "POST" }),
};

const DEV = "/auth/dev/usuarios";

/** CRUD sin inicio de sesión (backend: routers/dev_usuarios.py). Solo para desarrollo. */
export const devUsuariosApi: GestionUsuariosApi = {
  listar: (filtros) => api<Usuario[]>(`${DEV}${consulta(filtros)}`),
  crear: (datos) => api<UsuarioConPassword>(DEV, { method: "POST", body: datos }),
  modificar: (id, datos) => api<Usuario>(`${DEV}/${id}`, { method: "PUT", body: datos }),
  darDeBaja: (id) => api<Usuario>(`${DEV}/${id}`, { method: "DELETE" }),
  reactivar: (id) => api<Usuario>(`${DEV}/${id}/reactivar`, { method: "POST" }),
};
