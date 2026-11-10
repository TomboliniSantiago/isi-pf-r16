import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { asientosApi, etiquetaEstado, type Asiento } from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { formatearFechaContable, formatearImporte } from "../../api/planCuentas";
import { etiquetaEstadoCompra, comprasApi, type Compra } from "../../api/compras";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  idCompra: number;
  onCerrar: () => void;
}

/** CUU-002 paso 8: el comprobante y su asiento contable disponibles para consulta. */
export function DetalleCompra({ idCompra, onCerrar }: Props) {
  const [compra, setCompra] = useState<Compra | null>(null);
  const [asiento, setAsiento] = useState<Asiento | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    comprasApi
      .obtener(idCompra)
      .then(async (v) => {
        setCompra(v);
        if (v.asiento) setAsiento(await asientosApi.obtener(v.asiento.id_asiento));
      })
      .catch((err) => setError(mensajeDeError(err)));
  }, [idCompra]);

  const importe = (v: string | null) => formatearImporte(v ?? 0);

  return (
    <Modal
      titulo={compra ? `Compra ${compra.tipo_comprobante} ${compra.numero}` : "Compra"}
      onCerrar={onCerrar}
      ancho
      pie={
        <button type="button" className="boton boton-secundario" onClick={onCerrar}>
          Cerrar
        </button>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      {!compra && !error && <p className="texto-secundario">Cargando…</p>}
      {compra && (
        <>
          <dl className="ficha ficha-doble">
            <dt>Proveedor</dt>
            <dd>
              {compra.proveedor?.razon_social} <span className="texto-secundario">{compra.proveedor?.cuit}</span>
            </dd>
            <dt>Estado</dt>
            <dd>{etiquetaEstadoCompra(compra.estado)}</dd>
            <dt>Fecha de emisión</dt>
            <dd>{formatearFechaContable(compra.fecha_emision)}</dd>
            <dt>Fecha contable</dt>
            <dd>{formatearFechaContable(compra.fecha_contable)}</dd>
            <dt>Condición de pago</dt>
            <dd>{compra.condicion_compra ?? "—"}</dd>
            <dt>Moneda</dt>
            <dd>{compra.moneda ?? "—"}</dd>
            <dt>Neto gravado</dt>
            <dd>{importe(compra.importe_neto_gravado)}</dd>
            <dt>IVA</dt>
            <dd>{importe(compra.importe_iva)}</dd>
            <dt>Otros impuestos</dt>
            <dd>{importe(compra.importe_otros_impuestos)}</dd>
            <dt>Total</dt>
            <dd>
              <strong>{importe(compra.importe_total)}</strong>
            </dd>
          </dl>

          <h3 className="subtitulo">Asiento contable</h3>
          {!compra.asiento && (
            <p className="texto-secundario">
              {compra.estado === "PENDIENTE"
                ? "La compra está pendiente: todavía no tiene asiento ni efecto contable."
                : "La compra no tiene asiento contable."}
            </p>
          )}
          {asiento && (
            <>
              <p>
                Asiento N° {asiento.numero_asiento} del {formatearFechaContable(asiento.fecha)} ·{" "}
                {etiquetaEstado(asiento.estado)}
                {compra.asiento?.revertido_por && <> · revertido por el asiento N° {compra.asiento.revertido_por}</>} ·{" "}
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
