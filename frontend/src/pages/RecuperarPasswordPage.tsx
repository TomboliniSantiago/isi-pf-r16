import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../api/auth";
import { mensajeDeError } from "../api/client";
import { Alerta } from "../components/Alerta";
import { IngresoCodigo } from "../components/IngresoCodigo";
import { Marca } from "../components/Marca";
import { ReglasPassword, cumplePolitica } from "../components/ReglasPassword";
import type { Desafio } from "../types";

/** CUU-015 camino 1.a: restablecer la contraseña validando la identidad con un código por correo. */
export function RecuperarPasswordPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [desafio, setDesafio] = useState<Desafio | null>(null);
  const [codigo, setCodigo] = useState("");
  const [nueva, setNueva] = useState("");
  const [confirmacion, setConfirmacion] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const coinciden = nueva === confirmacion;

  async function solicitar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      setDesafio(await authApi.recuperarPassword(email));
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function confirmar(e: FormEvent) {
    e.preventDefault();
    if (!desafio) return;
    if (!coinciden) {
      setError("La confirmación no coincide con la nueva contraseña.");
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      await authApi.confirmarRecupero(desafio.desafio, codigo, nueva);
      navigate("/login", {
        replace: true,
        state: { aviso: "La contraseña se restableció correctamente. Inicie sesión con la nueva contraseña." },
      });
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <div className="pagina-centrada">
      <div className="pagina-centrada-marca">
        <Marca />
      </div>

      {desafio === null ? (
        <form className="tarjeta tarjeta-angosta" onSubmit={solicitar} noValidate>
          <h1>Restablecer contraseña</h1>
          <p className="texto-secundario">
            Ingrese su correo corporativo. Le enviaremos un código para validar su identidad.
          </p>
          {error && <Alerta tipo="error">{error}</Alerta>}
          <label className="campo">
            <span>Correo corporativo</span>
            <input type="email" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} autoFocus />
          </label>
          <button type="submit" className="boton boton-primario boton-bloque" disabled={enviando || !email}>
            {enviando ? "Enviando…" : "Enviar código"}
          </button>
          <div className="tarjeta-acciones-secundarias">
            <Link to="/login">Volver al inicio de sesión</Link>
          </div>
        </form>
      ) : (
        <form className="tarjeta tarjeta-angosta" onSubmit={confirmar} noValidate>
          <h1>Restablecer contraseña</h1>
          {error && <Alerta tipo="error">{error}</Alerta>}
          <IngresoCodigo
            desafio={desafio}
            codigo={codigo}
            onCodigo={setCodigo}
            onReenviado={setDesafio}
            onError={setError}
          />
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
          <button
            type="submit"
            className="boton boton-primario boton-bloque"
            disabled={enviando || codigo.length !== 6 || !cumplePolitica(nueva) || !coinciden}
          >
            {enviando ? "Guardando…" : "Restablecer contraseña"}
          </button>
          <div className="tarjeta-acciones-secundarias">
            <Link to="/login">Volver al inicio de sesión</Link>
          </div>
        </form>
      )}
    </div>
  );
}
