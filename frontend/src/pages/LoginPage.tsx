import { useState, type FormEvent } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { mensajeDeError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { Marca } from "../components/Marca";

export function LoginPage() {
  const { usuario, iniciarSesion } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to="/" replace />;

  async function enviar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      const u = await iniciarSesion(email, password);
      const desde = (location.state as { desde?: string } | null)?.desde ?? "/";
      navigate(u.debe_cambiar_password ? "/cambiar-password" : desde, { replace: true });
    } catch (err) {
      setError(mensajeDeError(err));
      setPassword("");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="login">
      <section className="login-panel" aria-hidden="true">
        <Marca grande />
        <p className="login-lema">Gestión contable inteligente, trazable y segura.</p>
        <ul className="login-puntos">
          <li>Registro contable con partida doble</li>
          <li>Comprobantes digitalizados con OCR</li>
          <li>Validación fiscal con ARCA</li>
        </ul>
      </section>

      <section className="login-formulario">
        <form className="tarjeta login-tarjeta" onSubmit={enviar} noValidate>
          <h1>Iniciar sesión</h1>
          <p className="texto-secundario">Ingrese con su correo corporativo.</p>

          {error && <Alerta tipo="error">{error}</Alerta>}

          <label className="campo">
            <span>Correo corporativo</span>
            <input
              type="email"
              autoComplete="username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />
          </label>
          <label className="campo">
            <span>Contraseña</span>
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <button type="submit" className="boton boton-primario boton-bloque" disabled={enviando || !email || !password}>
            {enviando ? "Verificando…" : "Ingresar"}
          </button>
          <p className="texto-ayuda">¿Olvidó su contraseña? Solicite el restablecimiento al administrador del sistema.</p>
        </form>
      </section>
    </div>
  );
}
