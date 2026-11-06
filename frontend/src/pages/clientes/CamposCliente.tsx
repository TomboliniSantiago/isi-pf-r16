import { CONDICIONES_IVA, type ClienteDatos, type CondicionIva } from "../../api/clientes";

interface Props {
  datos: ClienteDatos;
  onCambio: (datos: ClienteDatos) => void;
  /** En el alta el CUIT ya se validó contra el padrón y no se edita acá. */
  cuitEditable: boolean;
}

/** Campos del cliente compartidos por el alta y la modificación. */
export function CamposCliente({ datos, onCambio, cuitEditable }: Props) {
  const cambiar = (campo: keyof ClienteDatos) => (valor: string) => onCambio({ ...datos, [campo]: valor });

  return (
    <>
      <div className="campos-fila">
        <label className="campo">
          <span>CUIT</span>
          <input
            className="codigo-cuenta"
            value={datos.cuit}
            onChange={(e) => cambiar("cuit")(e.target.value)}
            readOnly={!cuitEditable}
            required
          />
        </label>
        <label className="campo">
          <span>Condición frente al IVA</span>
          <select value={datos.condicion_iva} onChange={(e) => cambiar("condicion_iva")(e.target.value as CondicionIva)}>
            {CONDICIONES_IVA.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="campo">
        <span>Razón social</span>
        <input value={datos.razon_social} onChange={(e) => cambiar("razon_social")(e.target.value)} maxLength={255} required />
      </label>
      <label className="campo">
        <span>Domicilio</span>
        <input value={datos.domicilio} onChange={(e) => cambiar("domicilio")(e.target.value)} maxLength={255} required />
      </label>
      <div className="campos-fila">
        <label className="campo">
          <span>Localidad</span>
          <input value={datos.localidad} onChange={(e) => cambiar("localidad")(e.target.value)} maxLength={255} />
        </label>
        <label className="campo">
          <span>Provincia</span>
          <input value={datos.provincia} onChange={(e) => cambiar("provincia")(e.target.value)} maxLength={255} />
        </label>
      </div>
    </>
  );
}
