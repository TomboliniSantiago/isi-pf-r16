import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import type { Rol } from "../types";
import { useAuth } from "./AuthContext";

interface Props {
  roles?: Rol[];
  children: ReactNode;
}

export function RutaProtegida({ roles, children }: Props) {
  const { usuario, cargando } = useAuth();
  const location = useLocation();

  if (cargando) return <div className="pantalla-carga">Cargando…</div>;
  if (!usuario) return <Navigate to="/login" replace state={{ desde: location.pathname }} />;
  if (usuario.debe_cambiar_password && location.pathname !== "/cambiar-password") {
    return <Navigate to="/cambiar-password" replace />;
  }
  if (roles && !roles.includes(usuario.nivel_acceso as Rol)) return <Navigate to="/sin-permiso" replace />;
  return <>{children}</>;
}
