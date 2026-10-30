import { Link } from "react-router-dom";

export function SinPermisoPage() {
  return (
    <section className="tarjeta tarjeta-angosta">
      <h1>Acceso restringido</h1>
      <p className="texto-secundario">Su perfil no tiene permisos para acceder a esta sección.</p>
      <Link to="/" className="boton boton-primario">
        Volver al inicio
      </Link>
    </section>
  );
}
