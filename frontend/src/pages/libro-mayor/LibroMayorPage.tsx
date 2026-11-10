import { useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { etiquetaOrigen } from "../../api/asientos";
import { mensajeDeError } from "../../api/client";
import { formatearSaldo, libroMayorApi, type CuentaMayor, type LibroMayor } from "../../api/libroMayor";
import { formatearFechaContable, formatearImporte, planCuentasApi, type Cuenta } from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";

function primerDiaDelAnio(): string {
  return `${new Date().getFullYear()}-01-01`;
}

/** CUU-006 Consultar Libro Mayor: movimientos y saldos de una cuenta o de las cuentas de un rubro. */
export function LibroMayorPage() {
  const [parametros, setParametros] = useSearchParams();
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [idCuenta, setIdCuenta] = useState(parametros.get("cuenta") ?? "");
  const [desde, setDesde] = useState(primerDiaDelAnio());
  const [hasta, setHasta] = useState("");
  const [mayor, setMayor] = useState<LibroMayor | null>(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    planCuentasApi
      .listar()
      .then(setCuentas)
      .catch((err) => setError(mensajeDeError(err)));
  }, []);

  useEffect(() => {
    if (!idCuenta) {
      setMayor(null);
      return;
    }
    const consulta = ++ultimaConsulta.current;
    setCargando(true);
    libroMayorApi
      .consultar(Number(idCuenta), desde || undefined, hasta || undefined)
      .then((r) => {
        if (consulta === ultimaConsulta.current) {
          setMayor(r);
          setError(null);
        }
      })
      .catch((err) => consulta === ultimaConsulta.current && setError(mensajeDeError(err)))
      .finally(() => consulta === ultimaConsulta.current && setCargando(false));
  }, [idCuenta, desde, hasta]);

  function elegirCuenta(valor: string) {
    setIdCuenta(valor);
    setParametros(valor ? { cuenta: valor } : {}, { replace: true });
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Libro Mayor</h1>
          <p className="texto-secundario">Movimientos y saldos de cada cuenta, calculados desde los asientos contabilizados.</p>
        </div>
      </div>

      <section className="tarjeta tarjeta-tabla">
        <div className="filtros filtros-mayor">
          <label className="campo">
            <span>Cuenta o rubro</span>
            <select value={idCuenta} onChange={(e) => elegirCuenta(e.target.value)}>
              <option value="">— Seleccione una cuenta —</option>
              {cuentas.map((c) => (
                <option key={c.id_cuenta} value={c.id_cuenta}>
                  {"  ".repeat(Math.max(c.nivel - 1, 0))}
                  {c.codigo} · {c.nombre}
                  {c.imputable ? "" : " (rubro)"}
                  {c.activa ? "" : " (dada de baja)"}
                </option>
              ))}
            </select>
          </label>
          <label className="campo">
            <span>Desde</span>
            <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
          </label>
          <label className="campo">
            <span>Hasta</span>
            <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
          </label>
        </div>
        {error && <Alerta tipo="error">{error}</Alerta>}
        {!idCuenta && (
          <p className="tabla-vacia">Seleccione una cuenta, o un rubro para ver todas sus cuentas, y el período a consultar.</p>
        )}
        {cargando && <div className="tabla-cargando">Cargando…</div>}
      </section>

      {mayor && idCuenta && (
        <>
          {!mayor.imputable && (
            <section className="tarjeta resumen-mayor">
              <h2>
                <span className="codigo-cuenta">{mayor.codigo}</span> {mayor.nombre}
              </h2>
              <dl className="ficha ficha-doble">
                <dt>Saldo inicial</dt>
                <dd>{formatearSaldo(mayor.saldo_inicial)}</dd>
                <dt>Saldo final</dt>
                <dd>
                  <strong>{formatearSaldo(mayor.saldo_final)}</strong>
                </dd>
                <dt>Total Debe</dt>
                <dd>{formatearImporte(mayor.total_debe)}</dd>
                <dt>Total Haber</dt>
                <dd>{formatearImporte(mayor.total_haber)}</dd>
              </dl>
              {mayor.cuentas.length === 0 && (
                <p className="texto-secundario">Las cuentas del rubro no tienen saldo ni movimientos en el período.</p>
              )}
            </section>
          )}
          {mayor.cuentas.map((c) => (
            <MayorDeCuenta key={c.id_cuenta} cuenta={c} desde={mayor.desde} />
          ))}
        </>
      )}
    </>
  );
}

function MayorDeCuenta({ cuenta, desde }: { cuenta: CuentaMayor; desde: string | null }) {
  return (
    <section className="tarjeta tarjeta-tabla mayor-cuenta">
      <div className="mayor-encabezado">
        <h2>
          <span className="codigo-cuenta">{cuenta.codigo}</span> {cuenta.nombre}
          {!cuenta.activa && <span className="etiqueta etiqueta-baja">Dada de baja</span>}
        </h2>
        <span className="texto-secundario">Saldo final: {formatearSaldo(cuenta.saldo_final)}</span>
      </div>
      {cuenta.movimientos.length === 0 && (
        <Alerta tipo="aviso">
          No existen movimientos en el período. Saldo inicial arrastrado: {formatearSaldo(cuenta.saldo_inicial)}.
        </Alerta>
      )}
      <div className="tabla-contenedor">
        <table className="tabla tabla-compacta">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Asiento</th>
              <th>Comprobante</th>
              <th>Concepto</th>
              <th className="col-importe">Debe</th>
              <th className="col-importe">Haber</th>
              <th className="col-importe">Saldo</th>
            </tr>
          </thead>
          <tbody>
            <tr className="fila-saldo">
              <td>{desde ? formatearFechaContable(desde) : "—"}</td>
              <td>—</td>
              <td>—</td>
              <td>Saldo anterior</td>
              <td />
              <td />
              <td className="col-importe">{formatearSaldo(cuenta.saldo_inicial)}</td>
            </tr>
            {cuenta.movimientos.map((m, i) => (
              <tr key={`${m.id_asiento}-${i}`}>
                <td>{formatearFechaContable(m.fecha)}</td>
                <td className="codigo-cuenta">N° {m.numero_asiento}</td>
                <td>
                  {m.id_venta ? (
                    <Link to={`/ventas?venta=${m.id_venta}`}>{m.referencia ?? "Venta"}</Link>
                  ) : (
                    (m.referencia ?? etiquetaOrigen(m.tipo_origen))
                  )}
                </td>
                <td>
                  {m.concepto}
                  {m.estado === "ANULADO" && <span className="etiqueta etiqueta-baja">Anulado</span>}
                </td>
                <td className="col-importe">{Number(m.debe) ? formatearImporte(m.debe) : ""}</td>
                <td className="col-importe">{Number(m.haber) ? formatearImporte(m.haber) : ""}</td>
                <td className="col-importe">{formatearSaldo(m.saldo)}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td colSpan={4}>Totales del período</td>
              <td className="col-importe">{formatearImporte(cuenta.total_debe)}</td>
              <td className="col-importe">{formatearImporte(cuenta.total_haber)}</td>
              <td className="col-importe">{formatearSaldo(cuenta.saldo_final)}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </section>
  );
}
