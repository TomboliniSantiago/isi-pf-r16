import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { etiquetaRol, formatearFecha } from "../types";

export function InicioPage() {
  const { usuario } = useAuth();
  const location = useLocation();
  const [aviso, setAviso] = useState((location.state as { aviso?: string } | null)?.aviso ?? null);

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Hola, {usuario?.nombre_usuario}</h1>
          <p className="texto-secundario">Panel principal de EugenIA.</p>
        </div>
      </div>

      {aviso && (
        <Alerta tipo="exito" onCerrar={() => setAviso(null)}>
          {aviso}
        </Alerta>
      )}

      <div className="grilla-tarjetas">
        <div className="tarjeta tarjeta-dato">
          <span className="tarjeta-dato-etiqueta">Perfil</span>
          <span className="tarjeta-dato-valor">{etiquetaRol(usuario?.nivel_acceso ?? null)}</span>
        </div>
        <div className="tarjeta tarjeta-dato">
          <span className="tarjeta-dato-etiqueta">Correo</span>
          <span className="tarjeta-dato-valor tarjeta-dato-texto">{usuario?.email}</span>
        </div>
        <div className="tarjeta tarjeta-dato">
          <span className="tarjeta-dato-etiqueta">Ingreso actual</span>
          <span className="tarjeta-dato-valor tarjeta-dato-texto">{formatearFecha(usuario?.ultimo_acceso ?? null)}</span>
        </div>
      </div>

      {usuario?.nivel_acceso === "ADMINISTRADOR" && (
        <section className="tarjeta">
          <h2>Administración</h2>
          <p className="texto-secundario">Alta, modificación y baja de usuarios del sistema.</p>
          <Link to="/usuarios" className="boton boton-primario">
            Gestionar usuarios
          </Link>
        </section>
      )}
    </>
  );
}
