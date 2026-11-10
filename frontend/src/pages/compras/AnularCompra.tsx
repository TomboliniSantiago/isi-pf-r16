import { useState } from "react";
import { mensajeDeError } from "../../api/client";
import { formatearImporte } from "../../api/planCuentas";
import { comprasApi, type Compra } from "../../api/compras";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  compra: Compra;
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/** Anulación de una compra: sin edición destructiva, el asiento se revierte con un contra-asiento. */
export function AnularCompra({ compra, onCerrar, onListo }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const contabilizada = compra.estado === "CONTABILIZADA";

  async function anular() {
    setError(null);
    setEnviando(true);
    try {
      const r = await comprasApi.anular(compra.id_compra);
      onListo(
        r.asiento?.revertido_por
          ? `La compra ${r.tipo_comprobante} ${r.numero} fue anulada con el contra-asiento N° ${r.asiento.revertido_por}.`
          : `La compra ${r.tipo_comprobante} ${r.numero} fue anulada.`,
      );
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo="Anular compra"
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
          {compra.tipo_comprobante} {compra.numero}
        </strong>{" "}
        · {compra.proveedor?.razon_social} · {formatearImporte(compra.importe_total ?? 0)}
      </p>
      <Alerta tipo="aviso">
        {contabilizada
          ? `La compra no se borra: su asiento N° ${compra.asiento?.numero_asiento} se revertirá con un contra-asiento en el Libro Diario y la compra quedará anulada.`
          : "La compra pendiente no tiene efecto contable: quedará anulada y se conservará en el historial."}
      </Alerta>
    </Modal>
  );
}
