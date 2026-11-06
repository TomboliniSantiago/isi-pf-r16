import { useEffect, useState } from "react";
import { clientesApi, type Cliente } from "../../api/clientes";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  cliente: Cliente;
  accion: "baja" | "reactivar";
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/** Baja (CUU-007 2.c): verifica que no haya comprobantes pendientes antes de pedir la confirmación. */
export function EstadoCliente({ cliente, accion, onCerrar, onListo }: Props) {
  const esBaja = accion === "baja";
  const [verificacion, setVerificacion] = useState<{ ok: boolean; mensaje: string } | null>(
    esBaja ? null : { ok: true, mensaje: "El cliente volverá a estar disponible para registrar ventas." },
  );
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (!esBaja) return;
    clientesApi
      .verificarBaja(cliente.id_cliente)
      .then((r) => setVerificacion({ ok: true, mensaje: `${r.mensaje} Puede darse de baja.` }))
      .catch((err) => setVerificacion({ ok: false, mensaje: mensajeDeError(err) }));
  }, [cliente.id_cliente, esBaja]);

  async function confirmar() {
    setError(null);
    setEnviando(true);
    try {
      if (esBaja) {
        await clientesApi.darDeBaja(cliente.id_cliente);
        onListo(`El cliente ${cliente.razon_social} fue dado de baja. Sus datos y comprobantes se conservan.`);
      } else {
        await clientesApi.reactivar(cliente.id_cliente);
        onListo(`El cliente ${cliente.razon_social} fue reactivado.`);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  const puedeConfirmar = verificacion?.ok === true;

  return (
    <Modal
      titulo={esBaja ? "Dar de baja cliente" : "Reactivar cliente"}
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
        <span className="codigo-cuenta">{cliente.codigo}</span> · <strong>{cliente.razon_social}</strong> ({cliente.cuit})
      </p>
      {error && <Alerta tipo="error">{error}</Alerta>}
      {verificacion === null ? (
        <p className="texto-secundario">Verificando comprobantes pendientes…</p>
      ) : (
        <Alerta tipo={verificacion.ok ? "aviso" : "error"}>{verificacion.mensaje}</Alerta>
      )}
    </Modal>
  );
}
