import { Link } from "react-router-dom";
import { devUsuariosApi } from "../api/usuarios";
import { Alerta } from "../components/Alerta";
import { Marca } from "../components/Marca";
import { UsuariosPage } from "./UsuariosPage";

/** Gestión de usuarios sin inicio de sesión (backend: /api/auth/dev/usuarios). Solo para desarrollo. */
export function DevUsuariosPage() {
  return (
    <div className="app">
      <header className="barra-superior">
        <span className="barra-marca">
          <Marca />
        </span>
        <div className="barra-usuario">
          <span className="etiqueta etiqueta-dev">Modo desarrollo</span>
          <Link to="/login" className="boton boton-claro boton-chico">
            Iniciar sesión
          </Link>
        </div>
      </header>
      <main className="contenido contenido-sin-menu">
        <Alerta tipo="aviso">
          Esta pantalla no requiere inicio de sesión: cualquiera con acceso a la aplicación puede crear, modificar y dar
          de baja usuarios. Las operaciones quedan auditadas como &quot;sin_sesion&quot;. Usar solo en el entorno local.
        </Alerta>
        <UsuariosPage api={devUsuariosApi} />
      </main>
    </div>
  );
}
