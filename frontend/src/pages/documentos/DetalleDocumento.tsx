import { Link } from "react-router-dom";
import { etiquetaEstadoDocumento, nivelConfianza, type Documento } from "../../api/documentos";
import { Modal } from "../../components/Modal";
import { VistaArchivo } from "./VistaArchivo";

interface Props {
  documento: Documento;
  onCerrar: () => void;
}

/** CUU-016 paso 9: trazabilidad entre el archivo original, los datos extraídos, las correcciones y el comprobante. */
export function DetalleDocumento({ documento, onCerrar }: Props) {
  const comprobante = documento.comprobante;
  const enlace = comprobante
    ? comprobante.tabla === "COMPRA"
      ? `/compras?compra=${comprobante.id}`
      : `/ventas?venta=${comprobante.id}`
    : null;
  return (
    <Modal
      titulo={`Documento N° ${documento.id_documento}: ${documento.nombre_archivo ?? ""}`}
      onCerrar={onCerrar}
      ancho
      pie={
        <button type="button" className="boton boton-secundario" onClick={onCerrar}>
          Cerrar
        </button>
      }
    >
      <div className="revision-documento">
        <VistaArchivo idDocumento={documento.id_documento} tipoContenido={documento.tipo_contenido} nombre={documento.nombre_archivo} />
        <div>
          <dl className="ficha ficha-doble">
            <dt>Estado</dt>
            <dd>{etiquetaEstadoDocumento(documento.estado)}</dd>
            <dt>Operación</dt>
            <dd>{documento.operacion === "COMPRA" ? "Compra" : "Venta"}</dd>
            <dt>Cargado por</dt>
            <dd>{documento.usuario ?? "—"}</dd>
            <dt>Lectura</dt>
            <dd>
              {documento.motor_ocr === "pdf-texto" ? "Texto del PDF" : documento.motor_ocr === "tesseract" ? "OCR (Tesseract)" : "Carga manual"}
            </dd>
            <dt>Comprobante</dt>
            <dd>{enlace ? <Link to={enlace}>Ver {comprobante?.tabla === "COMPRA" ? "compra" : "venta"} y su asiento</Link> : "—"}</dd>
          </dl>
          <table className="tabla tabla-compacta tabla-revision">
            <thead>
              <tr>
                <th>Campo</th>
                <th>Extraído</th>
                <th>Confianza</th>
                <th>Definitivo</th>
              </tr>
            </thead>
            <tbody>
              {documento.campos.map((c) => (
                <tr key={c.campo}>
                  <th>{c.etiqueta}</th>
                  <td>{c.valor_extraido ?? "—"}</td>
                  <td>
                    <span className={`confianza confianza-${nivelConfianza(c.confianza, documento.umbral_confianza)}`}>
                      {Math.round(Number(c.confianza ?? 0) * 100)}%
                    </span>
                  </td>
                  <td>
                    {c.valor_final ?? "—"}
                    {c.corregido && <span className="etiqueta etiqueta-pendiente">Corregido</span>}
                    {c.revisado && !c.corregido && <span className="etiqueta etiqueta-neutra">Revisado</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Modal>
  );
}
