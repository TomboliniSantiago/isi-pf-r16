import { useEffect, useState } from "react";
import { proveedoresApi, type Proveedor } from "../../api/proveedores";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  proveedor: Proveedor;
  accion: "baja" | "reactivar";
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/** Baja (CUU-008 2.b): verifica que no haya comprobantes pendientes antes de pedir la confirmación. */
export function EstadoProveedor({ proveedor, accion, onCerrar, onListo }: Props) {
  const esBaja = accion === "baja";
  const [verificacion, setVerificacion] = useState<{ ok: boolean; mensaje: string } | null>(
    esBaja ? null : { ok: true, mensaje: "El proveedor volverá a estar disponible para registrar compras." },
  );
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (!esBaja) return;
    proveedoresApi
      .verificarBaja(proveedor.id_proveedor)
      .then((r) => setVerificacion({ ok: true, mensaje: `${r.mensaje} Puede darse de baja.` }))
      .catch((err) => setVerificacion({ ok: false, mensaje: mensajeDeError(err) }));
  }, [proveedor.id_proveedor, esBaja]);

  async function confirmar() {
    setError(null);
    setEnviando(true);
    try {
      if (esBaja) {
        await proveedoresApi.darDeBaja(proveedor.id_proveedor);
        onListo(`El proveedor ${proveedor.razon_social} fue dado de baja. Sus datos y comprobantes se conservan.`);
      } else {
        await proveedoresApi.reactivar(proveedor.id_proveedor);
        onListo(`El proveedor ${proveedor.razon_social} fue reactivado.`);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  const puedeConfirmar = verificacion?.ok === true;

  return (
    <Modal
      titulo={esBaja ? "Dar de baja proveedor" : "Reactivar proveedor"}
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
        <span className="codigo-cuenta">{proveedor.codigo}</span> · <strong>{proveedor.razon_social}</strong> ({proveedor.cuit})
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
