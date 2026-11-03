import { useState, type FormEvent } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { mensajeDeError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { IngresoCodigo } from "../components/IngresoCodigo";
import { Marca } from "../components/Marca";
import type { Desafio } from "../types";

interface EstadoNavegacion {
  desde?: string;
  aviso?: string;
}

export function LoginPage() {
  const { usuario, iniciarSesion, verificarCodigo } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const estado = (location.state as EstadoNavegacion | null) ?? {};
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [desafio, setDesafio] = useState<Desafio | null>(null);
  const [codigo, setCodigo] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [aviso, setAviso] = useState(estado.aviso ?? null);
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to="/" replace />;

  async function enviarCredenciales(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setAviso(null);
    setEnviando(true);
    try {
      setDesafio(await iniciarSesion(email, password));
      setCodigo("");
    } catch (err) {
      setError(mensajeDeError(err));
      setPassword("");
    } finally {
      setEnviando(false);
    }
  }

  async function enviarCodigo(e: FormEvent) {
    e.preventDefault();
    if (!desafio) return;
    setError(null);
    setEnviando(true);
    try {
      const u = await verificarCodigo(desafio.desafio, codigo);
      navigate(u.debe_cambiar_password ? "/cambiar-password" : (estado.desde ?? "/"), { replace: true });
    } catch (err) {
      setError(mensajeDeError(err));
      setCodigo("");
      setEnviando(false);
    }
  }

  function volver() {
    setDesafio(null);
    setPassword("");
    setCodigo("");
    setError(null);
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
        {desafio === null ? (
          <form className="tarjeta login-tarjeta" onSubmit={enviarCredenciales} noValidate>
            <h1>Iniciar sesión</h1>
            <p className="texto-secundario">Ingrese con su correo corporativo.</p>

            {aviso && <Alerta tipo="exito">{aviso}</Alerta>}
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
              {enviando ? "Verificando…" : "Continuar"}
            </button>
            <p className="texto-ayuda">
              <Link to="/recuperar-password">¿Olvidó su contraseña?</Link>
            </p>
            <p className="texto-ayuda login-dev">
              <Link to="/dev/usuarios">Gestionar usuarios sin iniciar sesión (desarrollo)</Link>
            </p>
          </form>
        ) : (
          <form className="tarjeta login-tarjeta" onSubmit={enviarCodigo} noValidate>
            <h1>Verificación en dos pasos</h1>
            {error && <Alerta tipo="error">{error}</Alerta>}
            <IngresoCodigo
              desafio={desafio}
              codigo={codigo}
              onCodigo={setCodigo}
              onReenviado={setDesafio}
              onError={setError}
            />
            <button type="submit" className="boton boton-primario boton-bloque" disabled={enviando || codigo.length !== 6}>
              {enviando ? "Verificando…" : "Ingresar"}
            </button>
            <div className="tarjeta-acciones-secundarias">
              <button type="button" className="boton-enlace" onClick={volver}>
                Volver e ingresar con otra cuenta
              </button>
            </div>
          </form>
        )}
      </section>
    </div>
  );
}
