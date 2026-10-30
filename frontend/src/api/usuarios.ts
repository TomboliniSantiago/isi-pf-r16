import type { Rol, Usuario, UsuarioConPassword, UsuarioDatos } from "../types";
import { api } from "./client";

export interface FiltrosUsuarios {
  buscar?: string;
  activo?: boolean;
  rol?: Rol;
}

export const usuariosApi = {
  listar: (filtros: FiltrosUsuarios) => {
    const params = new URLSearchParams();
    if (filtros.buscar) params.set("buscar", filtros.buscar);
    if (filtros.activo !== undefined) params.set("activo", String(filtros.activo));
    if (filtros.rol) params.set("rol", filtros.rol);
    const query = params.toString();
    return api<Usuario[]>(`/usuarios${query ? `?${query}` : ""}`);
  },
  crear: (datos: UsuarioDatos) => api<UsuarioConPassword>("/usuarios", { method: "POST", body: datos }),
  modificar: (id: number, datos: UsuarioDatos) => api<Usuario>(`/usuarios/${id}`, { method: "PUT", body: datos }),
  darDeBaja: (id: number) => api<Usuario>(`/usuarios/${id}/baja`, { method: "POST" }),
  reactivar: (id: number) => api<Usuario>(`/usuarios/${id}/reactivar`, { method: "POST" }),
  restablecerPassword: (id: number) =>
    api<UsuarioConPassword>(`/usuarios/${id}/restablecer-password`, { method: "POST" }),
};
