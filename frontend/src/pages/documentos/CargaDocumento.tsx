import { useState, type FormEvent } from "react";
import { mensajeDeError } from "../../api/client";
import { documentosApi, type Documento, type OperacionDocumento } from "../../api/documentos";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  onCerrar: () => void;
  onCargado: (documento: Documento) => void;
}

const ACEPTADOS = ".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg";

/** CUU-016 pasos 1-2 / 2.a: el usuario selecciona el comprobante y el sistema lo procesa con OCR/NLP. */
export function CargaDocumento({ onCerrar, onCargado }: Props) {
  const [operacion, setOperacion] = useState<OperacionDocumento>("COMPRA");
  const [archivo, setArchivo] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function cargar(e: FormEvent) {
    e.preventDefault();
    if (!archivo) {
      setError("Seleccione el archivo del comprobante.");
      return;
    }
    setError(null);
    setEnviando(true);
    try {
      onCargado(await documentosApi.cargar(archivo, operacion));
    } catch (err) {
      setError(mensajeDeError(err)); // 2.a: formato no soportado → el usuario elige otro archivo
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo="Cargar comprobante digital"
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-carga" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Procesando…" : "Procesar comprobante"}
          </button>
        </>
      }
    >
      <form id="form-carga" onSubmit={cargar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <fieldset className="campo opciones-operacion">
          <legend>El comprobante es una</legend>
          <label>
            <input type="radio" checked={operacion === "COMPRA"} onChange={() => setOperacion("COMPRA")} /> Compra (factura de
            un proveedor)
          </label>
          <label>
            <input type="radio" checked={operacion === "VENTA"} onChange={() => setOperacion("VENTA")} /> Venta (factura
            emitida a un cliente)
          </label>
        </fieldset>
        <label className="campo">
          <span>Archivo (PDF, PNG o JPG)</span>
          <input type="file" accept={ACEPTADOS} onChange={(e) => setArchivo(e.target.files?.[0] ?? null)} required />
        </label>
        <p className="texto-secundario">
          El sistema guarda el archivo original y extrae sus datos. Ningún dato se contabiliza sin su revisión y confirmación.
        </p>
      </form>
    </Modal>
  );
}
