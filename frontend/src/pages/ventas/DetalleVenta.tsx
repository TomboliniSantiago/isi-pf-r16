import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { asientosApi, etiquetaEstado, type Asiento } from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { documentosApi } from "../../api/documentos";
import { formatearFechaContable, formatearImporte } from "../../api/planCuentas";
import { etiquetaEstadoVenta, ventasApi, type Venta } from "../../api/ventas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  idVenta: number;
  onCerrar: () => void;
}

/** CUU-001 paso 8: el comprobante y su asiento contable disponibles para consulta. */
export function DetalleVenta({ idVenta, onCerrar }: Props) {
  const [venta, setVenta] = useState<Venta | null>(null);
  const [asiento, setAsiento] = useState<Asiento | null>(null);
  const [error, setError] = useState<string | null>(null);
  // CUU-016: documento digital del que surgió el comprobante, si lo hay.
  const [idDocumento, setIdDocumento] = useState<number | null>(null);

  useEffect(() => {
    ventasApi
      .obtener(idVenta)
      .then(async (v) => {
        setVenta(v);
        if (v.asiento) setAsiento(await asientosApi.obtener(v.asiento.id_asiento));
      })
      .catch((err) => setError(mensajeDeError(err)));
    documentosApi
      .listar({ tabla_asociada: "VENTA", id_registro: idVenta })
      .then((docs) => setIdDocumento(docs[0]?.id_documento ?? null))
      .catch(() => setIdDocumento(null));
  }, [idVenta]);

  const importe = (v: string | null) => formatearImporte(v ?? 0);

  return (
    <Modal
      titulo={venta ? `Venta ${venta.tipo_comprobante} ${venta.numero}` : "Venta"}
      onCerrar={onCerrar}
      ancho
      pie={
        <button type="button" className="boton boton-secundario" onClick={onCerrar}>
          Cerrar
        </button>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      {!venta && !error && <p className="texto-secundario">Cargando…</p>}
      {venta && (
        <>
          <dl className="ficha ficha-doble">
            <dt>Cliente</dt>
            <dd>
              {venta.cliente?.razon_social} <span className="texto-secundario">{venta.cliente?.cuit}</span>
            </dd>
            <dt>Estado</dt>
            <dd>{etiquetaEstadoVenta(venta.estado)}</dd>
            <dt>Fecha de emisión</dt>
            <dd>{formatearFechaContable(venta.fecha_emision)}</dd>
            <dt>Fecha contable</dt>
            <dd>{formatearFechaContable(venta.fecha_contable)}</dd>
            <dt>Condición de cobro</dt>
            <dd>{venta.condicion_venta ?? "—"}</dd>
            <dt>Moneda</dt>
            <dd>{venta.moneda ?? "—"}</dd>
            <dt>Neto gravado</dt>
            <dd>{importe(venta.importe_neto_gravado)}</dd>
            <dt>IVA</dt>
            <dd>{importe(venta.importe_iva)}</dd>
            <dt>Otros impuestos</dt>
            <dd>{importe(venta.importe_otros_impuestos)}</dd>
            <dt>Total</dt>
            <dd>
              <strong>{importe(venta.importe_total)}</strong>
            </dd>
            <dt>CAE</dt>
            <dd>{venta.cae ?? "Sin validar con ARCA"}</dd>
          </dl>

          {idDocumento && (
            <p>
              <Link to={`/comprobantes-digitales?documento=${idDocumento}`}>Ver el comprobante digital original</Link>
            </p>
          )}
          <h3 className="subtitulo">Asiento contable</h3>
          {!venta.asiento && (
            <p className="texto-secundario">
              {venta.estado === "PENDIENTE"
                ? "La venta está pendiente: todavía no tiene asiento ni efecto contable."
                : "La venta no tiene asiento contable."}
            </p>
          )}
          {asiento && (
            <>
              <p>
                Asiento N° {asiento.numero_asiento} del {formatearFechaContable(asiento.fecha)} ·{" "}
                {etiquetaEstado(asiento.estado)}
                {venta.asiento?.revertido_por && <> · revertido por el asiento N° {venta.asiento.revertido_por}</>} ·{" "}
                <Link to="/libro-diario">Ver en el Libro Diario</Link>
              </p>
              <div className="tabla-contenedor">
                <table className="tabla tabla-compacta">
                  <thead>
                    <tr>
                      <th>Cuenta</th>
                      <th className="col-importe">Debe</th>
                      <th className="col-importe">Haber</th>
                    </tr>
                  </thead>
                  <tbody>
                    {asiento.lineas.map((l) => (
                      <tr key={l.id_detalle_asiento}>
                        <td className={Number(l.haber) ? "cuenta-haber" : undefined}>
                          <span className="codigo-cuenta">{l.codigo}</span> {l.nombre}
                        </td>
                        <td className="col-importe">{Number(l.debe) ? formatearImporte(l.debe) : ""}</td>
                        <td className="col-importe">{Number(l.haber) ? formatearImporte(l.haber) : ""}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr>
                      <td>Totales</td>
                      <td className="col-importe">{formatearImporte(asiento.total_debe)}</td>
                      <td className="col-importe">{formatearImporte(asiento.total_haber)}</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </>
          )}
        </>
      )}
    </Modal>
  );
}
