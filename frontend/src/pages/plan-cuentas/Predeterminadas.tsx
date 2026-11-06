import { useEffect, useState } from "react";
import { mensajeDeError } from "../../api/client";
import { esCoherente, planCuentasApi, type Cuenta, type Predeterminada } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";

interface Props {
  cuentas: Cuenta[];
  puedeEditar: boolean;
}

/** Cuentas que usarán los asientos automáticos de ventas y compras (alcance 70%, sección 2.2). */
export function Predeterminadas({ cuentas, puedeEditar }: Props) {
  const [items, setItems] = useState<Predeterminada[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [guardando, setGuardando] = useState<string | null>(null);

  const imputables = cuentas.filter((c) => c.activa && c.imputable);

  useEffect(() => {
    planCuentasApi
      .predeterminadas()
      .then(setItems)
      .catch((err) => setError(mensajeDeError(err)));
  }, []);

  async function asignar(clave: string, valor: string) {
    setError(null);
    setExito(null);
    setGuardando(clave);
    try {
      const actualizado = await planCuentasApi.asignarPredeterminada(clave, valor ? Number(valor) : null);
      setItems((prev) => prev.map((p) => (p.clave === clave ? actualizado : p)));
      setExito(`Se actualizó la cuenta predeterminada para ${actualizado.descripcion.toLowerCase()}.`);
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setGuardando(null);
    }
  }

  return (
    <section className="tarjeta">
      <h2>Cuentas predeterminadas</h2>
      <p className="texto-secundario">
        Se usarán para generar automáticamente los asientos de ventas y compras. Para cada uso solo se ofrecen cuentas
        activas, imputables y del tipo y naturaleza que corresponden.
      </p>
      {error && <Alerta tipo="error">{error}</Alerta>}
      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}
      <div className="tabla-contenedor">
        <table className="tabla">
          <thead>
            <tr>
              <th>Uso</th>
              <th>Requisito</th>
              <th>Cuenta asignada</th>
            </tr>
          </thead>
          <tbody>
            {items.map((p) => (
              <tr key={p.clave}>
                <td className="celda-principal">{p.descripcion}</td>
                <td className="texto-secundario">{p.requisito}</td>
                <td>
                  {puedeEditar ? (
                    <select
                      className="select-tabla"
                      value={p.cuenta?.id_cuenta ?? ""}
                      onChange={(e) => asignar(p.clave, e.target.value)}
                      disabled={guardando === p.clave}
                    >
                      <option value="">— Sin asignar —</option>
                      {/* La cuenta ya asignada se muestra aunque no cumpla la regla (datos heredados), para poder reemplazarla. */}
                      {imputables.filter((c) => esCoherente(c, p) || c.id_cuenta === p.cuenta?.id_cuenta).map((c) => (
                        <option key={c.id_cuenta} value={c.id_cuenta}>
                          {c.codigo} · {c.nombre}
                        </option>
                      ))}
                    </select>
                  ) : p.cuenta ? (
                    `${p.cuenta.codigo} · ${p.cuenta.nombre}`
                  ) : (
                    <span className="texto-secundario">Sin asignar</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
