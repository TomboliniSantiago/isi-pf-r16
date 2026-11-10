import { useState } from "react";
import { asientosApi, type Asiento } from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { formatearImporte } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  asiento: Asiento;
  accion: "anular" | "confirmar";
  onCerrar: () => void;
  onListo: (mensaje: string) => void;
}

/** Anulación (CUU-003 3.b) y contabilización de un asiento pendiente, con confirmación previa. */
export function AccionAsiento({ asiento, accion, onCerrar, onListo }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const esAnulacion = accion === "anular";
  const pendiente = asiento.estado === "BORRADOR";
  const descripcion = asiento.numero_asiento ? `asiento N° ${asiento.numero_asiento}` : "asiento pendiente";

  async function ejecutar() {
    setError(null);
    setEnviando(true);
    try {
      if (!esAnulacion) {
        const r = await asientosApi.confirmar(asiento.id_asiento);
        onListo(`El asiento se contabilizó con el N° ${r.numero_asiento}.`);
      } else if (pendiente) {
        await asientosApi.anular(asiento.id_asiento);
        onListo("El asiento pendiente fue descartado.");
      } else {
        const contra = await asientosApi.anular(asiento.id_asiento);
        onListo(`El ${descripcion} fue anulado con el contra-asiento N° ${contra.numero_asiento}.`);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo={esAnulacion ? (pendiente ? "Descartar asiento pendiente" : "Anular asiento") : "Contabilizar asiento"}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button
            type="button"
            className={`boton ${esAnulacion ? "boton-peligro" : "boton-primario"}`}
            onClick={ejecutar}
            disabled={enviando}
          >
            {enviando ? "Procesando…" : esAnulacion ? (pendiente ? "Descartar" : "Anular") : "Contabilizar"}
          </button>
        </>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      <p>
        <strong>{asiento.concepto}</strong> · {formatearImporte(asiento.total_debe)}
      </p>
      <Alerta tipo="aviso">
        {!esAnulacion
          ? "Se validará nuevamente que el asiento esté balanceado y se le asignará el próximo número del Libro Diario."
          : pendiente
            ? "El asiento pendiente no tiene efecto contable: quedará anulado y se conservará en el historial."
            : "El asiento no se borra: se registrará un contra-asiento con el Debe y el Haber invertidos, y el original quedará anulado."}
      </Alerta>
    </Modal>
  );
}
