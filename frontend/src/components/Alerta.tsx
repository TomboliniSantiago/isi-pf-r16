import type { ReactNode } from "react";

interface Props {
  tipo: "error" | "exito" | "aviso";
  children: ReactNode;
  onCerrar?: () => void;
}

export function Alerta({ tipo, children, onCerrar }: Props) {
  return (
    <div className={`alerta alerta-${tipo}`} role={tipo === "error" ? "alert" : "status"}>
      <span>{children}</span>
      {onCerrar && (
        <button type="button" className="alerta-cerrar" onClick={onCerrar} aria-label="Cerrar aviso">
          ×
        </button>
      )}
    </div>
  );
}
