import { useEffect, useState } from "react";
import { clientesApi, type ClienteDetalle, type Comprobante } from "../../api/clientes";
import { mensajeDeError } from "../../api/client";
import { formatearFechaContable, formatearImporte } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

/** CUU-007 2.b: datos del cliente e historial de comprobantes asociados. */
export function DetalleCliente({ idCliente, onCerrar }: { idCliente: number; onCerrar: () => void }) {
  const [detalle, setDetalle] = useState<ClienteDetalle | null>(null);
  const [comprobantes, setComprobantes] = useState<Comprobante[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([clientesApi.obtener(idCliente), clientesApi.comprobantes(idCliente)])
      .then(([d, c]) => {
        setDetalle(d);
        setComprobantes(c);
      })
      .catch((err) => setError(mensajeDeError(err)));
  }, [idCliente]);

  return (
    <Modal
      titulo="Detalle del cliente"
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
          <dl className="ficha ficha-doble">
            <dt>Código</dt>
            <dd className="codigo-cuenta">{detalle.codigo}</dd>
            <dt>CUIT</dt>
            <dd className="codigo-cuenta">{detalle.cuit}</dd>
            <dt>Razón social</dt>
            <dd>{detalle.razon_social}</dd>
            <dt>Condición IVA</dt>
            <dd>{detalle.condicion_iva}</dd>
            <dt>Domicilio</dt>
            <dd>{detalle.domicilio}</dd>
            <dt>Localidad</dt>
            <dd>{[detalle.localidad, detalle.provincia].filter(Boolean).join(", ") || "—"}</dd>
            <dt>Estado</dt>
            <dd>{detalle.activo ? "Activo" : "Dado de baja"}</dd>
            <dt>Comprobantes</dt>
            <dd>
              {detalle.cantidad_comprobantes}
              {detalle.comprobantes_pendientes > 0 && ` (${detalle.comprobantes_pendientes} pendiente/s)`}
            </dd>
          </dl>

          <h3 className="subtitulo">Comprobantes asociados</h3>
          {comprobantes && comprobantes.length === 0 ? (
            <p className="texto-secundario">El cliente no tiene comprobantes registrados.</p>
          ) : (
            <div className="tabla-contenedor">
              <table className="tabla tabla-compacta">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Comprobante</th>
                    <th className="col-importe">Total</th>
                    <th>CAE</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {comprobantes?.map((c) => (
                    <tr key={c.id_venta}>
                      <td>{formatearFechaContable(c.fecha_emision)}</td>
                      <td>
                        {c.tipo_comprobante} <span className="codigo-cuenta">{c.numero}</span>
                      </td>
                      <td className="col-importe">
                        {c.importe_total ? formatearImporte(c.importe_total) : "—"}
                        {c.moneda && c.moneda !== "ARS" ? ` ${c.moneda}` : ""}
                      </td>
                      <td className="codigo-cuenta">{c.cae ?? "—"}</td>
                      <td>
                        {c.pendiente ? (
                          <span className="etiqueta etiqueta-pendiente">{c.cae ? "Sin asentar" : "Pendiente de validación"}</span>
                        ) : (
                          <span className="etiqueta etiqueta-activo">Procesado</span>
                        )}
                      </td>
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
