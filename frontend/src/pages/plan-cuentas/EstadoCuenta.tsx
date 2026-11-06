import { useEffect, useState } from "react";
import { mensajeDeError } from "../../api/client";
import { planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  cuenta: Cuenta;
  accion: "baja" | "reactivar";
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/**
 * Baja lógica (CUU-005 2.b): primero verifica que la cuenta pueda darse de baja (sin movimientos
 * ni dependientes activas) y recién entonces pide la confirmación. También resuelve la reactivación.
 */
export function EstadoCuenta({ cuenta, accion, onCerrar, onListo }: Props) {
  const esBaja = accion === "baja";
  const [verificacion, setVerificacion] = useState<{ ok: boolean; mensaje: string } | null>(
    esBaja ? null : { ok: true, mensaje: "La cuenta volverá a estar disponible para imputar movimientos." },
  );
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (!esBaja) return;
    planCuentasApi
      .verificarBaja(cuenta.id_cuenta)
      .then((r) => setVerificacion({ ok: true, mensaje: `${r.mensaje} Puede darse de baja.` }))
      .catch((err) => setVerificacion({ ok: false, mensaje: mensajeDeError(err) }));
  }, [cuenta.id_cuenta, esBaja]);

  async function confirmar() {
    setError(null);
    setEnviando(true);
    try {
      if (esBaja) {
        await planCuentasApi.darDeBaja(cuenta.id_cuenta);
        onListo(`La cuenta ${cuenta.codigo} fue dada de baja. Su información histórica se conserva.`);
      } else {
        await planCuentasApi.reactivar(cuenta.id_cuenta);
        onListo(`La cuenta ${cuenta.codigo} fue reactivada.`);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  const puedeConfirmar = verificacion?.ok === true;

  return (
    <Modal
      titulo={esBaja ? "Dar de baja cuenta" : "Reactivar cuenta"}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            {puedeConfirmar ? "Cancelar" : "Cerrar"}
          </button>
          {puedeConfirmar && (
            <button
              type="button"
              className={`boton ${esBaja ? "boton-peligro" : "boton-primario"}`}
              onClick={confirmar}
              disabled={enviando}
            >
              {enviando ? "Procesando…" : esBaja ? "Dar de baja" : "Reactivar"}
            </button>
          )}
        </>
      }
    >
      <p>
        <span className="codigo-cuenta">{cuenta.codigo}</span> · <strong>{cuenta.nombre}</strong>
      </p>
      {error && <Alerta tipo="error">{error}</Alerta>}
      {verificacion === null ? (
        <p className="texto-secundario">Verificando movimientos y cuentas dependientes…</p>
      ) : (
        <Alerta tipo={verificacion.ok ? "aviso" : "error"}>{verificacion.mensaje}</Alerta>
      )}
    </Modal>
  );
}
