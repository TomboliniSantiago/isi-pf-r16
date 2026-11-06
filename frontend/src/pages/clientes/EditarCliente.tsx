import { useState, type FormEvent } from "react";
import { clientesApi, datosDe, type Cliente, type ClienteDatos } from "../../api/clientes";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { CamposCliente } from "./CamposCliente";

/** Modificación de cliente (CUU-007 2.a). El CUIT solo puede cambiarse si no tiene comprobantes. */
export function EditarCliente({
  cliente,
  onCerrar,
  onGuardado,
}: {
  cliente: Cliente;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
}) {
  const [datos, setDatos] = useState<ClienteDatos>(datosDe(cliente));
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function guardar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      await clientesApi.modificar(cliente.id_cliente, datos);
      onGuardado(`Los datos del cliente ${cliente.codigo} se actualizaron correctamente.`);
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo={`Modificar cliente ${cliente.codigo}`}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-editar-cliente" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Guardando…" : "Guardar cambios"}
          </button>
        </>
      }
    >
      <form id="form-editar-cliente" onSubmit={guardar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <CamposCliente datos={datos} onCambio={setDatos} cuitEditable />
      </form>
    </Modal>
  );
}
