import type { LoginRespuesta, Usuario } from "../types";
import { api } from "./client";

export const authApi = {
  login: (email: string, password: string) =>
    api<LoginRespuesta>("/auth/login", { method: "POST", body: { email, password } }),
  logout: () => api<void>("/auth/logout", { method: "POST" }),
  me: () => api<Usuario>("/auth/me"),
  cambiarPassword: (password_actual: string, password_nueva: string) =>
    api<Usuario>("/auth/cambiar-password", { method: "POST", body: { password_actual, password_nueva } }),
};
