import { useEffect, useState } from "react";
import { authApi } from "../api/auth";
import { mensajeDeError } from "../api/client";
import type { Desafio } from "../types";

interface Props {
  desafio: Desafio;
  codigo: string;
  onCodigo: (codigo: string) => void;
  /** Se llama con el nuevo desafío tras un reenvío exitoso (CUU-015 6.a.3). */
  onReenviado: (desafio: Desafio) => void;
  onError: (mensaje: string | null) => void;
}

/** Campo para el código de 6 dígitos enviado por correo, con reenvío temporizado. */
export function IngresoCodigo({ desafio, codigo, onCodigo, onReenviado, onError }: Props) {
  const [espera, setEspera] = useState(desafio.reenvio_en);
  const [reenviando, setReenviando] = useState(false);
  const [reenviado, setReenviado] = useState(false);

  useEffect(() => {
    setEspera(desafio.reenvio_en);
    const intervalo = setInterval(() => setEspera((s) => (s > 0 ? s - 1 : 0)), 1000);
    return () => clearInterval(intervalo);
  }, [desafio]);

  async function reenviar() {
    onError(null);
    setReenviando(true);
    try {
      onReenviado(await authApi.reenviarCodigo(desafio.desafio));
      onCodigo("");
      setReenviado(true);
    } catch (err) {
      onError(mensajeDeError(err));
    } finally {
      setReenviando(false);
    }
  }

  return (
    <div className="ingreso-codigo">
      <p className="texto-secundario">
        Enviamos un código de 6 dígitos a <strong>{desafio.destino}</strong>. Vence en{" "}
        {Math.round(desafio.expira_en / 60)} minutos.
        {reenviado && " Se envió un código nuevo; el anterior ya no es válido."}
      </p>
      <label className="campo">
        <span>Código de verificación</span>
        <input
          className="campo-codigo"
          inputMode="numeric"
          autoComplete="one-time-code"
          maxLength={6}
          value={codigo}
          onChange={(e) => onCodigo(e.target.value.replace(/\D/g, ""))}
          autoFocus
        />
      </label>
      <p className="texto-ayuda">
        ¿No lo recibió?{" "}
        <button type="button" className="boton-enlace" onClick={reenviar} disabled={espera > 0 || reenviando}>
          {reenviando ? "Enviando…" : espera > 0 ? `Reenviar código en ${espera} s` : "Reenviar código"}
        </button>
      </p>
    </div>
  );
}
