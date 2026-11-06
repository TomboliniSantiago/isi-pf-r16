import { useState, type FormEvent } from "react";
import { clientesApi, type ClienteDatos, type ClienteResumen, type CondicionIva } from "../../api/clientes";
import { mensajeDeError } from "../../api/client";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";
import { CamposCliente } from "./CamposCliente";

interface Props {
  onCerrar: () => void;
  onCreado: (mensaje: string) => void;
  onVerExistente: (cliente: ClienteResumen) => void;
}

/**
 * Alta de cliente (CUU-007 pasos 2-6): se ingresa el CUIT, el sistema consulta el padrón de ARCA
 * y detecta si ya existe un cliente con ese CUIT (4.a); luego el usuario completa y confirma.
 */
export function AltaCliente({ onCerrar, onCreado, onVerExistente }: Props) {
  const [cuit, setCuit] = useState("");
  const [datos, setDatos] = useState<ClienteDatos | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);
  const [existente, setExistente] = useState<ClienteResumen | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function consultar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setExistente(null);
    setEnviando(true);
    try {
      const r = await clientesApi.consultarCuit(cuit);
      if (r.cliente_existente) {
        setExistente(r.cliente_existente);
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
          : "El CUIT no figura en el padrón de ARCA: complete los datos del cliente.",
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
      const creado = await clientesApi.crear(datos);
      onCreado(`El cliente ${creado.razon_social} se registró con el código ${creado.codigo}.`);
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
        titulo="Nuevo cliente"
        onCerrar={onCerrar}
        pie={
          <>
            <button type="button" className="boton boton-secundario" onClick={otroCuit} disabled={enviando}>
              Cambiar CUIT
            </button>
            <button type="submit" form="form-alta-cliente" className="boton boton-primario" disabled={enviando}>
              {enviando ? "Guardando…" : "Confirmar alta"}
            </button>
          </>
        }
      >
        <form id="form-alta-cliente" onSubmit={confirmar}>
          {aviso && <Alerta tipo="aviso">{aviso}</Alerta>}
          {error && <Alerta tipo="error">{error}</Alerta>}
          <CamposCliente datos={datos} onCambio={setDatos} cuitEditable={false} />
        </form>
      </Modal>
    );
  }

  return (
    <Modal
      titulo="Nuevo cliente"
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
          Ingrese el CUIT del cliente. El sistema consulta el padrón de ARCA y completa los datos disponibles.
        </p>
        {error && <Alerta tipo="error">{error}</Alerta>}
        {existente && (
          <Alerta tipo="aviso">
            Ya existe un cliente con el CUIT {existente.cuit}: <strong>{existente.razon_social}</strong> ({existente.codigo}
            {existente.activo ? "" : ", dado de baja"}).{" "}
            <button type="button" className="boton-enlace" onClick={() => onVerExistente(existente)}>
              Ver cliente
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
