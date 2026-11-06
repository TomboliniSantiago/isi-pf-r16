import { useState, type FormEvent } from "react";
import { proveedoresApi, datosDe, type Proveedor, type ProveedorDatos } from "../../api/proveedores";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { CamposContribuyente } from "../../components/CamposContribuyente";

/** Modificación de proveedor (CUU-008 2.a). El CUIT solo puede cambiarse si no tiene comprobantes. */
export function EditarProveedor({
  proveedor,
  onCerrar,
  onGuardado,
}: {
  proveedor: Proveedor;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
}) {
  const [datos, setDatos] = useState<ProveedorDatos>(datosDe(proveedor));
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function guardar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      await proveedoresApi.modificar(proveedor.id_proveedor, datos);
      onGuardado(`Los datos del proveedor ${proveedor.codigo} se actualizaron correctamente.`);
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo={`Modificar proveedor ${proveedor.codigo}`}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-editar-proveedor" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Guardando…" : "Guardar cambios"}
          </button>
        </>
      }
    >
      <form id="form-editar-proveedor" onSubmit={guardar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <CamposContribuyente datos={datos} onCambio={setDatos} cuitEditable />
      </form>
    </Modal>
  );
}
