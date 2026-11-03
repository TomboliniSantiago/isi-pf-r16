import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { authApi } from "../api/auth";
import { onSesionExpirada, tokenStore } from "../api/client";
import type { Desafio, Usuario } from "../types";

interface AuthContexto {
  usuario: Usuario | null;
  cargando: boolean;
  /** Paso 1 del login: devuelve el desafío del código enviado por correo. */
  iniciarSesion: (email: string, password: string) => Promise<Desafio>;
  /** Paso 2 del login: valida el código e inicia la sesión. */
  verificarCodigo: (desafio: string, codigo: string) => Promise<Usuario>;
  cerrarSesion: () => Promise<void>;
  actualizarUsuario: (usuario: Usuario) => void;
}

const Contexto = createContext<AuthContexto | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    onSesionExpirada(() => {
      tokenStore.clear();
      setUsuario(null);
    });
    if (!tokenStore.get()) {
      setCargando(false);
      return;
    }
    authApi
      .me()
      .then(setUsuario)
      .catch(() => tokenStore.clear())
      .finally(() => setCargando(false));
  }, []);

  const iniciarSesion = useCallback((email: string, password: string) => authApi.login(email, password), []);

  const verificarCodigo = useCallback(async (desafio: string, codigo: string) => {
    const respuesta = await authApi.verificarLogin(desafio, codigo);
    tokenStore.set(respuesta.access_token);
    setUsuario(respuesta.usuario);
    return respuesta.usuario;
  }, []);

  const cerrarSesion = useCallback(async () => {
    try {
      await authApi.logout();
    } catch {
      /* aunque falle el registro en el servidor, la sesión local se cierra */
    } finally {
      tokenStore.clear();
      setUsuario(null);
    }
  }, []);

  const valor = useMemo(
    () => ({ usuario, cargando, iniciarSesion, verificarCodigo, cerrarSesion, actualizarUsuario: setUsuario }),
    [usuario, cargando, iniciarSesion, verificarCodigo, cerrarSesion],
  );
  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useAuth(): AuthContexto {
  const contexto = useContext(Contexto);
  if (!contexto) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return contexto;
}
