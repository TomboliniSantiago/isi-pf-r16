import { useState, type FormEvent } from "react";
import type { CondicionIva } from "../../api/contribuyentes";
import { proveedoresApi, type Proveedor, type ProveedorDatos, type ProveedorResumen } from "../../api/proveedores";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { CamposContribuyente } from "../../components/CamposContribuyente";

interface Props {
  onCerrar: () => void;
  onCreado: (mensaje: string, proveedor: Proveedor) => void;
  onVerExistente: (proveedor: ProveedorResumen) => void;
}

/**
 * Alta de proveedor (CUU-008 pasos 2-6): se ingresa el CUIT, el sistema consulta el padrón de ARCA
 * y detecta si ya existe un proveedor con ese CUIT (4.a); luego el usuario completa y confirma.
 */
export function AltaProveedor({ onCerrar, onCreado, onVerExistente }: Props) {
  const [cuit, setCuit] = useState("");
  const [datos, setDatos] = useState<ProveedorDatos | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);
  const [existente, setExistente] = useState<ProveedorResumen | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function consultar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setExistente(null);
    setEnviando(true);
    try {
      const r = await proveedoresApi.consultarCuit(cuit);
      if (r.proveedor_existente) {
        setExistente(r.proveedor_existente);
        return;
      }
      setDatos({
        cuit: r.cuit,
        razon_social: r.datos?.razon_social ?? "",
        condicion_iva: (r.datos?.condicion_iva as CondicionIva | undefined) ?? "Responsable Inscripto",
        domicilio: r.datos?.domicilio ?? "",
        localidad: r.datos?.localidad ?? "",
        provincia: r.datos?.provincia ?? "",
      });
      setAviso(
        r.en_padron
          ? "Datos obtenidos del padrón de ARCA. Verifíquelos y complete lo que falte antes de confirmar."
          : "El CUIT no figura en el padrón de ARCA: complete los datos del proveedor.",
      );
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function confirmar(e: FormEvent) {
    e.preventDefault();
    if (!datos) return;
    setError(null);
    setEnviando(true);
    try {
      const creado = await proveedoresApi.crear(datos);
      onCreado(`El proveedor ${creado.razon_social} se registró con el código ${creado.codigo}.`, creado);
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  function otroCuit() {
    setDatos(null);
    setExistente(null);
    setAviso(null);
    setError(null);
  }

  if (datos) {
    return (
      <Modal
        titulo="Nuevo proveedor"
        onCerrar={onCerrar}
        pie={
          <>
            <button type="button" className="boton boton-secundario" onClick={otroCuit} disabled={enviando}>
              Cambiar CUIT
            </button>
            <button type="submit" form="form-alta-proveedor" className="boton boton-primario" disabled={enviando}>
              {enviando ? "Guardando…" : "Confirmar alta"}
            </button>
          </>
        }
      >
        <form id="form-alta-proveedor" onSubmit={confirmar}>
          {aviso && <Alerta tipo="aviso">{aviso}</Alerta>}
          {error && <Alerta tipo="error">{error}</Alerta>}
          <CamposContribuyente datos={datos} onCambio={setDatos} cuitEditable={false} />
        </form>
      </Modal>
    );
  }

  return (
    <Modal
      titulo="Nuevo proveedor"
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-cuit" className="boton boton-primario" disabled={enviando || !cuit.trim()}>
            {enviando ? "Consultando…" : "Consultar padrón"}
          </button>
        </>
      }
    >
      <form id="form-cuit" onSubmit={consultar}>
        <p className="texto-secundario">
          Ingrese el CUIT del proveedor. El sistema consulta el padrón de ARCA y completa los datos disponibles.
        </p>
        {error && <Alerta tipo="error">{error}</Alerta>}
        {existente && (
          <Alerta tipo="aviso">
            Ya existe un proveedor con el CUIT {existente.cuit}: <strong>{existente.razon_social}</strong> ({existente.codigo}
            {existente.activo ? "" : ", dado de baja"}).{" "}
            <button type="button" className="boton-enlace" onClick={() => onVerExistente(existente)}>
              Ver proveedor
            </button>
          </Alerta>
        )}
        <label className="campo">
          <span>CUIT</span>
          <input
            className="codigo-cuenta"
            value={cuit}
            onChange={(e) => {
              setCuit(e.target.value);
              setExistente(null);
            }}
            placeholder="30-71234567-8"
            autoFocus
          />
        </label>
      </form>
    </Modal>
  );
}
