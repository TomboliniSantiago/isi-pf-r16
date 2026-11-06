import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { etiquetaRol } from "../types";
import { Marca } from "./Marca";

export function Layout() {
  const { usuario, cerrarSesion } = useAuth();
  const navigate = useNavigate();
  const esAdmin = usuario?.nivel_acceso === "ADMINISTRADOR";

  async function salir() {
    await cerrarSesion();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app">
      <header className="barra-superior">
        <Link to="/" className="barra-marca">
          <Marca />
        </Link>
        <div className="barra-usuario">
          <div className="barra-usuario-datos">
            <span className="barra-usuario-nombre">{usuario?.nombre_usuario}</span>
            <span className="barra-usuario-rol">{etiquetaRol(usuario?.nivel_acceso ?? null)}</span>
          </div>
          <Link to="/cambiar-password" className="boton boton-fantasma boton-chico">
            Cambiar contraseña
          </Link>
          <button type="button" className="boton boton-claro boton-chico" onClick={salir}>
            Cerrar sesión
          </button>
        </div>
      </header>

      <div className="app-cuerpo">
        <nav className="menu-lateral" aria-label="Navegación principal">
          <NavLink to="/" end className="menu-item">
            Inicio
          </NavLink>
          <span className="menu-seccion">Contabilidad</span>
          <NavLink to="/plan-cuentas" className="menu-item">
            Plan de cuentas
          </NavLink>
          <span className="menu-seccion">Comercial</span>
          <NavLink to="/clientes" className="menu-item">
            Clientes
          </NavLink>
          <NavLink to="/proveedores" className="menu-item">
            Proveedores
          </NavLink>
          {esAdmin && (
            <>
              <span className="menu-seccion">Administración</span>
              <NavLink to="/usuarios" className="menu-item">
                Usuarios
              </NavLink>
            </>
          )}
        </nav>
        <main className="contenido">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
