// Misma política que valida el backend (app/security.py).
const REGLAS: { texto: string; cumple: (p: string) => boolean }[] = [
  { texto: "Al menos 8 caracteres", cumple: (p) => p.length >= 8 },
  { texto: "Una letra mayúscula", cumple: (p) => /[A-ZÁÉÍÓÚÑ]/.test(p) },
  { texto: "Una letra minúscula", cumple: (p) => /[a-záéíóúñ]/.test(p) },
  { texto: "Un número", cumple: (p) => /\d/.test(p) },
];

export function cumplePolitica(password: string): boolean {
  return REGLAS.every((r) => r.cumple(password));
}

export function ReglasPassword({ password }: { password: string }) {
  return (
    <ul className="reglas">
      {REGLAS.map((r) => (
        <li key={r.texto} className={r.cumple(password) ? "regla-ok" : undefined}>
          {r.texto}
        </li>
      ))}
    </ul>
  );
}
