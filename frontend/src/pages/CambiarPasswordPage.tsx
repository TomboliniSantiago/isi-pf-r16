import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../api/auth";
import { mensajeDeError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { IngresoCodigo } from "../components/IngresoCodigo";
import { Marca } from "../components/Marca";
import { ReglasPassword, cumplePolitica } from "../components/ReglasPassword";
import type { Desafio } from "../types";

export function CambiarPasswordPage() {
  const { usuario, actualizarUsuario, cerrarSesion } = useAuth();
  const navigate = useNavigate();
  const [actual, setActual] = useState("");
  const [nueva, setNueva] = useState("");
  const [confirmacion, setConfirmacion] = useState("");
  const [desafio, setDesafio] = useState<Desafio | null>(null);
  const [codigo, setCodigo] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [solicitando, setSolicitando] = useState(false);

  // El cambio obligatorio de la contraseña temporal no pide código: ya se validó uno al iniciar sesión.
  const obligatorio = usuario?.debe_cambiar_password ?? false;
  const coinciden = nueva === confirmacion;
  const codigoListo = obligatorio || (desafio !== null && codigo.length === 6);

  async function solicitarCodigo() {
    setError(null);
    setSolicitando(true);
    try {
      setDesafio(await authApi.solicitarCodigoCambio());
      setCodigo("");
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setSolicitando(false);
    }
  }

  async function enviar(e: FormEvent) {
    e.preventDefault();
    if (!coinciden) {
      setError("La confirmación no coincide con la nueva contraseña.");
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      const actualizado = obligatorio
        ? await authApi.cambiarPassword(actual, nueva)
        : await authApi.cambiarPassword(actual, nueva, desafio?.desafio, codigo);
      actualizarUsuario(actualizado);
      navigate("/", { replace: true, state: { aviso: "La contraseña se actualizó correctamente." } });
    } catch (err) {
      setError(mensajeDeError(err));
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
        {obligatorio && <Alerta tipo="aviso">Debe reemplazar la contraseña temporal antes de continuar.</Alerta>}
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
        <ReglasPassword password={nueva} />
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

        {!obligatorio &&
          (desafio === null ? (
            <div className="bloque-codigo">
              <p className="texto-secundario">Para confirmar el cambio le enviaremos un código a su correo.</p>
              <button
                type="button"
                className="boton boton-secundario boton-bloque"
                onClick={solicitarCodigo}
                disabled={solicitando}
              >
                {solicitando ? "Enviando…" : "Enviar código a mi correo"}
              </button>
            </div>
          ) : (
            <div className="bloque-codigo">
              <IngresoCodigo
                desafio={desafio}
                codigo={codigo}
                onCodigo={setCodigo}
                onReenviado={setDesafio}
                onError={setError}
              />
            </div>
          ))}

        <button
          type="submit"
          className="boton boton-primario boton-bloque"
          disabled={enviando || !actual || !cumplePolitica(nueva) || !coinciden || !codigoListo}
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
