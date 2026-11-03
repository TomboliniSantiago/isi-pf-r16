import type { Desafio, LoginRespuesta, Usuario } from "../types";
import { api } from "./client";

export const authApi = {
  /** Paso 1: correo y contraseña. Si son correctos, el backend envía un código al correo. */
  login: (email: string, password: string) =>
    api<Desafio>("/auth/login", { method: "POST", body: { email, password } }),
  /** Paso 2: código recibido por correo. */
  verificarLogin: (desafio: string, codigo: string) =>
    api<LoginRespuesta>("/auth/login/verificar", { method: "POST", body: { desafio, codigo } }),
  reenviarCodigo: (desafio: string) => api<Desafio>("/auth/codigo/reenviar", { method: "POST", body: { desafio } }),
  recuperarPassword: (email: string) => api<Desafio>("/auth/recuperar-password", { method: "POST", body: { email } }),
  confirmarRecupero: (desafio: string, codigo: string, password_nueva: string) =>
    api<void>("/auth/recuperar-password/confirmar", { method: "POST", body: { desafio, codigo, password_nueva } }),
  logout: () => api<void>("/auth/logout", { method: "POST" }),
  me: () => api<Usuario>("/auth/me"),
  solicitarCodigoCambio: () => api<Desafio>("/auth/cambiar-password/codigo", { method: "POST" }),
  /** `desafio` y `codigo` son obligatorios salvo en el cambio de la contraseña temporal. */
  cambiarPassword: (password_actual: string, password_nueva: string, desafio?: string, codigo?: string) =>
    api<Usuario>("/auth/cambiar-password", {
      method: "POST",
      body: { password_actual, password_nueva, desafio, codigo },
    }),
};
