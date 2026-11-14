import { useEffect, useState } from "react";
import { mensajeDeError } from "../../api/client";
import { documentosApi } from "../../api/documentos";

interface Props {
  idDocumento: number;
  tipoContenido: string | null;
  nombre: string | null;
}

/** Muestra el archivo original del comprobante (PDF o imagen) junto a los datos extraídos. */
export function VistaArchivo({ idDocumento, tipoContenido, nombre }: Props) {
  const [url, setUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let creada: string | null = null;
    documentosApi
      .archivo(idDocumento)
      .then((blob) => {
        creada = URL.createObjectURL(blob);
        setUrl(creada);
      })
      .catch((err) => setError(mensajeDeError(err)));
    return () => {
      if (creada) URL.revokeObjectURL(creada);
    };
  }, [idDocumento]);

  if (error) return <p className="texto-secundario">{error}</p>;
  if (!url) return <p className="texto-secundario">Cargando el archivo…</p>;
  return (
    <div className="vista-archivo">
      {tipoContenido === "application/pdf" ? (
        <iframe src={url} title={nombre ?? "Comprobante"} />
      ) : (
        <img src={url} alt={nombre ?? "Comprobante"} />
      )}
      <a href={url} target="_blank" rel="noreferrer" className="boton-enlace">
        Abrir en otra pestaña
      </a>
    </div>
  );
}
