import { useState, type FormEvent } from "react";
import { mensajeDeError } from "../../api/client";
import {
  TIPOS,
  etiquetaNaturaleza,
  etiquetaTipo,
  planCuentasApi,
  type Cuenta,
  type CuentaDatos,
  type Naturaleza,
  type TipoCuenta,
} from "../../api/planCuentas";
import { Alerta } from "../../components/Alerta";
import { Modal } from "../../components/Modal";

interface Props {
  cuentas: Cuenta[];
  /** Cuenta a modificar; null para un alta. */
  cuenta: Cuenta | null;
  /** Padre sugerido al agregar una subcuenta. */
  padreInicial?: Cuenta | null;
  onCerrar: () => void;
  onGuardado: (mensaje: string) => void;
}

/**
 * Alta (CUU-005 pasos 2-6) y modificación (2.a) en dos pasos: el usuario completa los datos,
 * el sistema los valida y los muestra, y el usuario confirma.
 */
export function FormularioCuenta({ cuentas, cuenta, padreInicial = null, onCerrar, onGuardado }: Props) {
  const padreDe = (id: number | null) => cuentas.find((c) => c.id_cuenta === id) ?? null;

  const [datos, setDatos] = useState<CuentaDatos>({
    codigo: cuenta?.codigo ?? (padreInicial?.codigo ? `${padreInicial.codigo}.` : ""),
    nombre: cuenta?.nombre ?? "",
    tipo_cuenta: cuenta?.tipo_cuenta ?? padreInicial?.tipo_cuenta ?? "ACTIVO",
    naturaleza: cuenta?.naturaleza ?? null,
    imputable: cuenta?.imputable ?? false,
    id_cuenta_padre: cuenta?.id_cuenta_padre ?? padreInicial?.id_cuenta ?? null,
  });
  const [paso, setPaso] = useState<"datos" | "revisar">("datos");
  const [validacion, setValidacion] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // Posibles padres: rubros (no imputables) activos, excluida la propia cuenta.
  const padres = cuentas.filter((c) => c.activa && !c.imputable && c.id_cuenta !== cuenta?.id_cuenta);
  const padre = padreDe(datos.id_cuenta_padre);

  function cambiarPadre(valor: string) {
    const nuevo = valor ? padreDe(Number(valor)) : null;
    setDatos((d) => ({
      ...d,
      id_cuenta_padre: nuevo?.id_cuenta ?? null,
      tipo_cuenta: nuevo?.tipo_cuenta ?? d.tipo_cuenta,
      codigo: nuevo?.codigo && !cuenta ? `${nuevo.codigo}.` : d.codigo,
    }));
  }

  async function revisar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      const r = await planCuentasApi.validar(datos, cuenta?.id_cuenta);
      setValidacion(r.mensaje);
      setPaso("revisar");
    } catch (err) {
      setError(mensajeDeError(err));
    } finally {
      setEnviando(false);
    }
  }

  async function confirmar() {
    setError(null);
    setEnviando(true);
    try {
      if (cuenta) {
        await planCuentasApi.modificar(cuenta.id_cuenta, datos);
        onGuardado(`La cuenta ${datos.codigo} se modificó correctamente.`);
      } else {
        await planCuentasApi.crear(datos);
        onGuardado(`La cuenta ${datos.codigo} se creó correctamente.`);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setPaso("datos");
      setEnviando(false);
    }
  }

  const titulo = cuenta ? "Modificar cuenta" : "Nueva cuenta";

  if (paso === "revisar") {
    return (
      <Modal
        titulo={`${titulo}: confirmar`}
        onCerrar={onCerrar}
        pie={
          <>
            <button type="button" className="boton boton-secundario" onClick={() => setPaso("datos")} disabled={enviando}>
              Volver a editar
            </button>
            <button type="button" className="boton boton-primario" onClick={confirmar} disabled={enviando}>
              {enviando ? "Guardando…" : cuenta ? "Confirmar modificación" : "Confirmar alta"}
            </button>
          </>
        }
      >
        {error && <Alerta tipo="error">{error}</Alerta>}
        {validacion && <Alerta tipo="exito">{validacion}</Alerta>}
        <dl className="ficha">
          <dt>Cuenta padre</dt>
          <dd>{padre ? `${padre.codigo} · ${padre.nombre}` : "Sin cuenta padre (rubro principal)"}</dd>
          <dt>Código</dt>
          <dd className="codigo-cuenta">{datos.codigo}</dd>
          <dt>Denominación</dt>
          <dd>{datos.nombre}</dd>
          <dt>Tipo</dt>
          <dd>{etiquetaTipo(datos.tipo_cuenta)}</dd>
          <dt>Imputable</dt>
          <dd>{datos.imputable ? "Sí: recibe movimientos" : "No: agrupa otras cuentas"}</dd>
          <dt>Naturaleza</dt>
          <dd>{etiquetaNaturaleza(datos.naturaleza)}</dd>
        </dl>
      </Modal>
    );
  }

  return (
    <Modal
      titulo={titulo}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-cuenta" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Validando…" : "Revisar"}
          </button>
        </>
      }
    >
      <form id="form-cuenta" onSubmit={revisar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <label className="campo">
          <span>Cuenta padre</span>
          <select value={datos.id_cuenta_padre ?? ""} onChange={(e) => cambiarPadre(e.target.value)}>
            <option value="">— Sin cuenta padre (rubro principal) —</option>
            {padres.map((c) => (
              <option key={c.id_cuenta} value={c.id_cuenta}>
                {"  ".repeat(c.nivel - 1)}
                {c.codigo} · {c.nombre}
              </option>
            ))}
          </select>
        </label>
        <div className="campos-fila">
          <label className="campo">
            <span>Código</span>
            <input
              className="codigo-cuenta"
              value={datos.codigo}
              onChange={(e) => setDatos({ ...datos, codigo: e.target.value })}
              placeholder="1.1.1.01"
              required
              autoFocus
            />
          </label>
          <label className="campo">
            <span>Tipo</span>
            <select
              value={datos.tipo_cuenta}
              onChange={(e) => setDatos({ ...datos, tipo_cuenta: e.target.value as TipoCuenta })}
              disabled={padre !== null}
            >
              {TIPOS.map((t) => (
                <option key={t.valor} value={t.valor}>
                  {t.etiqueta}
                </option>
              ))}
            </select>
          </label>
        </div>
        {padre && <small className="texto-ayuda campo-nota">El tipo se toma de la cuenta padre.</small>}
        <label className="campo">
          <span>Denominación</span>
          <input
            value={datos.nombre}
            onChange={(e) => setDatos({ ...datos, nombre: e.target.value })}
            maxLength={255}
            required
          />
        </label>
        <label className="campo-check">
          <input
            type="checkbox"
            checked={datos.imputable}
            onChange={(e) => setDatos({ ...datos, imputable: e.target.checked })}
          />
          <span>
            Cuenta imputable <small className="texto-secundario">(recibe movimientos; no puede tener subcuentas)</small>
          </span>
        </label>
        <fieldset className="campo campo-opciones">
          <legend>Naturaleza{datos.imputable ? "" : " (opcional en rubros)"}</legend>
          {(["DEUDORA", "ACREEDORA"] as Naturaleza[]).map((n) => (
            <label key={n} className="campo-check">
              <input
                type="radio"
                name="naturaleza"
                checked={datos.naturaleza === n}
                onChange={() => setDatos({ ...datos, naturaleza: n })}
              />
              <span>{etiquetaNaturaleza(n)}</span>
            </label>
          ))}
          {!datos.imputable && datos.naturaleza && (
            <button type="button" className="boton-enlace" onClick={() => setDatos({ ...datos, naturaleza: null })}>
              Quitar
            </button>
          )}
        </fieldset>
      </form>
    </Modal>
  );
}
