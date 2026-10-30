import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../api/auth";
import { mensajeDeError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { Marca } from "../components/Marca";

// Misma política que valida el backend (app/security.py).
const REGLAS: { texto: string; cumple: (p: string) => boolean }[] = [
  { texto: "Al menos 8 caracteres", cumple: (p) => p.length >= 8 },
  { texto: "Una letra mayúscula", cumple: (p) => /[A-ZÁÉÍÓÚÑ]/.test(p) },
  { texto: "Una letra minúscula", cumple: (p) => /[a-záéíóúñ]/.test(p) },
  { texto: "Un número", cumple: (p) => /\d/.test(p) },
];

export function CambiarPasswordPage() {
  const { usuario, actualizarUsuario, cerrarSesion } = useAuth();
  const navigate = useNavigate();
  const [actual, setActual] = useState("");
  const [nueva, setNueva] = useState("");
  const [confirmacion, setConfirmacion] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const obligatorio = usuario?.debe_cambiar_password ?? false;
  const cumpleTodas = REGLAS.every((r) => r.cumple(nueva));
  const coinciden = nueva === confirmacion;

  async function enviar(e: FormEvent) {
    e.preventDefault();
    if (!coinciden) {
      setError("La confirmación no coincide con la nueva contraseña.");
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      actualizarUsuario(await authApi.cambiarPassword(actual, nueva));
      navigate("/", { replace: true, state: { aviso: "La contraseña se actualizó correctamente." } });
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function salir() {
    await cerrarSesion();
    navigate("/login", { replace: true });
  }

  return (
    <div className="pagina-centrada">
      <div className="pagina-centrada-marca">
        <Marca />
      </div>
      <form className="tarjeta tarjeta-angosta" onSubmit={enviar} noValidate>
        <h1>Cambiar contraseña</h1>
        {obligatorio && (
          <Alerta tipo="aviso">Debe reemplazar la contraseña temporal antes de continuar.</Alerta>
        )}
        {error && <Alerta tipo="error">{error}</Alerta>}

        <label className="campo">
          <span>{obligatorio ? "Contraseña temporal" : "Contraseña actual"}</span>
          <input
            type="password"
            autoComplete="current-password"
            value={actual}
            onChange={(e) => setActual(e.target.value)}
            autoFocus
          />
        </label>
        <label className="campo">
          <span>Nueva contraseña</span>
          <input type="password" autoComplete="new-password" value={nueva} onChange={(e) => setNueva(e.target.value)} />
        </label>
        <ul className="reglas">
          {REGLAS.map((r) => (
            <li key={r.texto} className={r.cumple(nueva) ? "regla-ok" : undefined}>
              {r.texto}
            </li>
          ))}
        </ul>
        <label className="campo">
          <span>Confirmar nueva contraseña</span>
          <input
            type="password"
            autoComplete="new-password"
            value={confirmacion}
            onChange={(e) => setConfirmacion(e.target.value)}
            aria-invalid={confirmacion !== "" && !coinciden}
          />
          {confirmacion !== "" && !coinciden && <small className="campo-error">Las contraseñas no coinciden.</small>}
        </label>

        <button
          type="submit"
          className="boton boton-primario boton-bloque"
          disabled={enviando || !actual || !cumpleTodas || !coinciden}
        >
          {enviando ? "Guardando…" : "Guardar contraseña"}
        </button>
        <div className="tarjeta-acciones-secundarias">
          {obligatorio ? (
            <button type="button" className="boton-enlace" onClick={salir}>
              Cerrar sesión
            </button>
          ) : (
            <Link to="/">Volver al inicio</Link>
          )}
        </div>
      </form>
    </div>
  );
}
