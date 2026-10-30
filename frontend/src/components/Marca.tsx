export function Marca({ grande = false }: { grande?: boolean }) {
  return (
    <span className={grande ? "marca marca-grande" : "marca"}>
      <svg viewBox="0 0 32 32" aria-hidden="true" className="marca-icono">
        <rect width="32" height="32" rx="6" fill="currentColor" opacity="0.15" />
        <path d="M10 8h12v3h-8.5v3.5H21v3h-7.5V21H22v3H10z" fill="currentColor" />
      </svg>
      <span>
        Eugen<strong>IA</strong>
      </span>
    </span>
  );
}
