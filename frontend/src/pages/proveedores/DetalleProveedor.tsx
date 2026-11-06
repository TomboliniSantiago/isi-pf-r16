import { useEffect, useState } from "react";
import { mensajeDeError } from "../../api/client";
import { formatearFechaContable, formatearImporte } from "../../api/planCuentas";
import { proveedoresApi, type Comprobante, type ProveedorDetalle } from "../../api/proveedores";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

/** CUU-008 2.c: datos del proveedor e historial de comprobantes de compra asociados. */
export function DetalleProveedor({ idProveedor, onCerrar }: { idProveedor: number; onCerrar: () => void }) {
  const [detalle, setDetalle] = useState<ProveedorDetalle | null>(null);
  const [comprobantes, setComprobantes] = useState<Comprobante[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([proveedoresApi.obtener(idProveedor), proveedoresApi.comprobantes(idProveedor)])
      .then(([d, c]) => {
        setDetalle(d);
        setComprobantes(c);
      })
      .catch((err) => setError(mensajeDeError(err)));
  }, [idProveedor]);

  return (
    <Modal
      titulo="Detalle del proveedor"
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
              {detalle.comprobantes_pendientes > 0 && ` (${detalle.comprobantes_pendientes} sin asentar)`}
            </dd>
          </dl>

          <h3 className="subtitulo">Comprobantes de compra</h3>
          {comprobantes && comprobantes.length === 0 ? (
            <p className="texto-secundario">El proveedor no tiene comprobantes registrados.</p>
          ) : (
            <div className="tabla-contenedor">
              <table className="tabla tabla-compacta">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Comprobante</th>
                    <th className="col-importe">Total</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {comprobantes?.map((c) => (
                    <tr key={c.id_compra}>
                      <td>{formatearFechaContable(c.fecha_emision)}</td>
                      <td>
                        {c.tipo_comprobante} <span className="codigo-cuenta">{c.numero}</span>
                      </td>
                      <td className="col-importe">
                        {c.importe_total ? formatearImporte(c.importe_total) : "—"}
                        {c.moneda && c.moneda !== "ARS" ? ` ${c.moneda}` : ""}
                      </td>
                      <td>
                        {c.pendiente ? (
                          <span className="etiqueta etiqueta-pendiente">Sin asentar</span>
                        ) : (
                          <span className="etiqueta etiqueta-activo">Asentado</span>
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
