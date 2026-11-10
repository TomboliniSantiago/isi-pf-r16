import { useState } from "react";
import { mensajeDeError } from "../../api/client";
import { formatearImporte } from "../../api/planCuentas";
import { ventasApi, type Venta } from "../../api/ventas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  venta: Venta;
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/** Anulación de una venta: sin edición destructiva, el asiento se revierte con un contra-asiento. */
export function AnularVenta({ venta, onCerrar, onListo }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const contabilizada = venta.estado === "CONTABILIZADA";

  async function anular() {
    setError(null);
    setEnviando(true);
    try {
      const r = await ventasApi.anular(venta.id_venta);
      onListo(
        r.asiento?.revertido_por
          ? `La venta ${r.tipo_comprobante} ${r.numero} fue anulada con el contra-asiento N° ${r.asiento.revertido_por}.`
          : `La venta ${r.tipo_comprobante} ${r.numero} fue anulada.`,
      );
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo="Anular venta"
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="button" className="boton boton-peligro" onClick={anular} disabled={enviando}>
            {enviando ? "Procesando…" : "Anular"}
          </button>
        </>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      <p>
        <strong>
          {venta.tipo_comprobante} {venta.numero}
        </strong>{" "}
        · {venta.cliente?.razon_social} · {formatearImporte(venta.importe_total ?? 0)}
      </p>
      <Alerta tipo="aviso">
        {contabilizada
          ? `La venta no se borra: su asiento N° ${venta.asiento?.numero_asiento} se revertirá con un contra-asiento en el Libro Diario y la venta quedará anulada.`
          : "La venta pendiente no tiene efecto contable: quedará anulada y se conservará en el historial."}
      </Alerta>
    </Modal>
  );
}
