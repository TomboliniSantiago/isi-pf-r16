import { useEffect, useState } from "react";
import { mensajeDeError } from "../../api/client";
import {
  etiquetaNaturaleza,
  etiquetaTipo,
  formatearFechaContable,
  formatearImporte,
  planCuentasApi,
  type CuentaDetalle,
  type Movimiento,
} from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

/** CUU-005 2.c: detalle de la cuenta, su ubicación en la jerarquía y sus movimientos. */
export function DetalleCuenta({ idCuenta, onCerrar }: { idCuenta: number; onCerrar: () => void }) {
  const [detalle, setDetalle] = useState<CuentaDetalle | null>(null);
  const [movimientos, setMovimientos] = useState<Movimiento[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([planCuentasApi.obtener(idCuenta), planCuentasApi.movimientos(idCuenta)])
      .then(([d, m]) => {
        setDetalle(d);
        setMovimientos(m);
      })
      .catch((err) => setError(mensajeDeError(err)));
  }, [idCuenta]);

  return (
    <Modal
      titulo="Detalle de la cuenta"
      onCerrar={onCerrar}
      ancho
      pie={
        <button type="button" className="boton boton-primario" onClick={onCerrar}>
          Cerrar
        </button>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      {!detalle && !error && <p className="texto-secundario">Cargando…</p>}
      {detalle && (
        <>
          <nav className="ruta-cuenta" aria-label="Ubicación en el Plan de Cuentas">
            {detalle.ruta.map((c) => (
              <span key={c.id_cuenta}>
                {c.codigo} {c.nombre}
              </span>
            ))}
            <strong>
              {detalle.codigo} {detalle.nombre}
            </strong>
          </nav>

          <dl className="ficha ficha-doble">
            <dt>Código</dt>
            <dd className="codigo-cuenta">{detalle.codigo}</dd>
            <dt>Denominación</dt>
            <dd>{detalle.nombre}</dd>
            <dt>Tipo</dt>
            <dd>{etiquetaTipo(detalle.tipo_cuenta)}</dd>
            <dt>Naturaleza</dt>
            <dd>{etiquetaNaturaleza(detalle.naturaleza)}</dd>
            <dt>Imputable</dt>
            <dd>{detalle.imputable ? "Sí" : "No"}</dd>
            <dt>Estado</dt>
            <dd>{detalle.activa ? "Activa" : "Dada de baja"}</dd>
            <dt>Cuentas dependientes</dt>
            <dd>{detalle.cantidad_hijas}</dd>
            <dt>Predeterminada para</dt>
            <dd>{detalle.predeterminada_para.length ? detalle.predeterminada_para.join(", ") : "—"}</dd>
          </dl>

          <h3 className="subtitulo">Movimientos</h3>
          {movimientos && movimientos.length === 0 ? (
            <p className="texto-secundario">La cuenta no tiene movimientos registrados.</p>
          ) : (
            <div className="tabla-contenedor">
              <table className="tabla tabla-compacta">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Asiento</th>
                    <th>Concepto</th>
                    <th>Estado</th>
                    <th className="col-importe">Debe</th>
                    <th className="col-importe">Haber</th>
                  </tr>
                </thead>
                <tbody>
                  {movimientos?.map((m) => (
                    <tr key={`${m.id_asiento}-${m.debe}-${m.haber}`}>
                      <td>{formatearFechaContable(m.fecha)}</td>
                      <td>{m.numero_asiento ?? "—"}</td>
                      <td>{m.concepto}</td>
                      <td>{m.estado}</td>
                      <td className="col-importe">{Number(m.debe) ? formatearImporte(m.debe) : ""}</td>
                      <td className="col-importe">{Number(m.haber) ? formatearImporte(m.haber) : ""}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </Modal>
  );
}
