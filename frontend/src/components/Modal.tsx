import { useEffect, type ReactNode } from "react";

interface Props {
  titulo: string;
  onCerrar: () => void;
  children: ReactNode;
  pie?: ReactNode;
  /** Ventana más ancha, para contenido tabular. */
  ancho?: boolean;
}

export function Modal({ titulo, onCerrar, children, pie, ancho = false }: Props) {
  useEffect(() => {
    const alPresionar = (e: KeyboardEvent) => {
      if (e.key === "Escape") onCerrar();
    };
    document.addEventListener("keydown", alPresionar);
    return () => document.removeEventListener("keydown", alPresionar);
  }, [onCerrar]);

  return (
    <div className="modal-fondo" onMouseDown={(e) => e.target === e.currentTarget && onCerrar()}>
      <div className={ancho ? "modal modal-ancho" : "modal"} role="dialog" aria-modal="true" aria-labelledby="modal-titulo">
        <div className="modal-encabezado">
          <h2 id="modal-titulo">{titulo}</h2>
          <button type="button" className="modal-cerrar" onClick={onCerrar} aria-label="Cerrar">
            ×
          </button>
        </div>
        <div className="modal-cuerpo">{children}</div>
        {pie && <div className="modal-pie">{pie}</div>}
      </div>
    </div>
  );
}
