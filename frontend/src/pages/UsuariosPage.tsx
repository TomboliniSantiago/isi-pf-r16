import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import { mensajeDeError } from "../api/client";
import { usuariosApi, type FiltrosUsuarios, type GestionUsuariosApi } from "../api/usuarios";
import { useAuth } from "../auth/AuthContext";
import { Alerta } from "../components/Alerta";
import { Modal } from "../components/Modal";
import { ROLES, etiquetaRol, formatearFecha, type Rol, type Usuario, type UsuarioDatos } from "../types";

type Estado = "" | "activos" | "baja";
type Accion = "baja" | "reactivar" | "restablecer";

type Dialogo =
  | { tipo: "formulario"; usuario: Usuario | null }
  | { tipo: "confirmar"; accion: Accion; usuario: Usuario }
  | { tipo: "password"; usuario: Usuario; password: string; titulo: string; mensaje: string };

const CONFIRMACIONES: Record<Accion, { titulo: string; texto: string; boton: string; peligro: boolean }> = {
  baja: {
    titulo: "Dar de baja usuario",
    texto: "El usuario no podrá iniciar sesión. Sus datos y su historial se conservan y puede reactivarse más adelante.",
    boton: "Dar de baja",
    peligro: true,
  },
  reactivar: {
    titulo: "Reactivar usuario",
    texto: "El usuario volverá a tener acceso al sistema con su perfil actual.",
    boton: "Reactivar",
    peligro: false,
  },
  restablecer: {
    titulo: "Restablecer contraseña",
    texto:
      "Se generará una nueva contraseña temporal y se desbloqueará la cuenta. La contraseña anterior dejará de funcionar.",
    boton: "Restablecer",
    peligro: false,
  },
};

export function UsuariosPage({ api = usuariosApi }: { api?: GestionUsuariosApi }) {
  const { usuario: actual } = useAuth();
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [errorCarga, setErrorCarga] = useState<string | null>(null);
  const [exito, setExito] = useState<string | null>(null);
  const [textoBusqueda, setTextoBusqueda] = useState("");
  const [buscar, setBuscar] = useState("");
  const [estado, setEstado] = useState<Estado>("activos");
  const [rol, setRol] = useState<Rol | "">("");
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);
  const ultimaConsulta = useRef(0);

  useEffect(() => {
    const t = setTimeout(() => setBuscar(textoBusqueda.trim()), 300);
    return () => clearTimeout(t);
  }, [textoBusqueda]);

  const cargar = useCallback(async () => {
    const consulta = ++ultimaConsulta.current;
    const filtros: FiltrosUsuarios = {
      buscar: buscar || undefined,
      activo: estado === "" ? undefined : estado === "activos",
      rol: rol || undefined,
    };
    setCargando(true);
    try {
      const resultado = await api.listar(filtros);
      if (consulta === ultimaConsulta.current) {
        setUsuarios(resultado);
        setErrorCarga(null);
      }
    } catch (err) {
      if (consulta === ultimaConsulta.current) setErrorCarga(mensajeDeError(err));
    } finally {
      if (consulta === ultimaConsulta.current) setCargando(false);
    }
  }, [api, buscar, estado, rol]);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const cerrarDialogo = useCallback(() => setDialogo(null), []);

  function informar(mensaje: string) {
    setExito(mensaje);
    void cargar();
  }

  return (
    <>
      <div className="encabezado-pagina">
        <div>
          <h1>Usuarios</h1>
          <p className="texto-secundario">Alta, modificación y baja de los usuarios del sistema.</p>
        </div>
        <button type="button" className="boton boton-primario" onClick={() => setDialogo({ tipo: "formulario", usuario: null })}>
          + Nuevo usuario
        </button>
      </div>

      {exito && (
        <Alerta tipo="exito" onCerrar={() => setExito(null)}>
          {exito}
        </Alerta>
      )}

      <section className="tarjeta tarjeta-tabla">
        <div className="filtros">
          <label className="campo campo-busqueda">
            <span>Buscar</span>
            <input
              type="search"
              placeholder="Nombre de usuario o correo"
              value={textoBusqueda}
              onChange={(e) => setTextoBusqueda(e.target.value)}
            />
          </label>
          <label className="campo">
            <span>Estado</span>
            <select value={estado} onChange={(e) => setEstado(e.target.value as Estado)}>
              <option value="activos">Activos</option>
              <option value="baja">Dados de baja</option>
              <option value="">Todos</option>
            </select>
          </label>
          <label className="campo">
            <span>Perfil</span>
            <select value={rol} onChange={(e) => setRol(e.target.value as Rol | "")}>
              <option value="">Todos</option>
              {ROLES.map((r) => (
                <option key={r.valor} value={r.valor}>
                  {r.etiqueta}
                </option>
              ))}
            </select>
          </label>
        </div>

        {errorCarga && <Alerta tipo="error">{errorCarga}</Alerta>}

        <div className="tabla-contenedor">
          <table className="tabla">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Correo</th>
                <th>Perfil</th>
                <th>Estado</th>
                <th>Último acceso</th>
                <th className="col-acciones">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => {
                const esActual = esUsuarioActual(u, actual);
                return (
                  <tr key={u.id_usuario}>
                    <td>
                      <span className="celda-principal">{u.nombre_usuario}</span>
                      {esActual && <span className="etiqueta etiqueta-neutra">Usted</span>}
                    </td>
                    <td>{u.email}</td>
                    <td>
                      <span className="etiqueta etiqueta-rol">{etiquetaRol(u.nivel_acceso)}</span>
                    </td>
                    <td>
                      <EstadoUsuario usuario={u} />
                    </td>
                    <td>{formatearFecha(u.ultimo_acceso)}</td>
                    <td className="col-acciones">
                      <div className="acciones">
                        <button type="button" className="boton-enlace" onClick={() => setDialogo({ tipo: "formulario", usuario: u })}>
                          Editar
                        </button>
                        {u.activo ? (
                          <>
                            {api.restablecerPassword && (
                              <button
                                type="button"
                                className="boton-enlace"
                                onClick={() => setDialogo({ tipo: "confirmar", accion: "restablecer", usuario: u })}
                              >
                                Restablecer contraseña
                              </button>
                            )}
                            {!esActual && (
                              <button
                                type="button"
                                className="boton-enlace boton-enlace-peligro"
                                onClick={() => setDialogo({ tipo: "confirmar", accion: "baja", usuario: u })}
                              >
                                Dar de baja
                              </button>
                            )}
                          </>
                        ) : (
                          <button
                            type="button"
                            className="boton-enlace"
                            onClick={() => setDialogo({ tipo: "confirmar", accion: "reactivar", usuario: u })}
                          >
                            Reactivar
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
              {!cargando && usuarios.length === 0 && (
                <tr>
                  <td colSpan={6} className="tabla-vacia">
                    No se encontraron usuarios con los filtros seleccionados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          {cargando && <div className="tabla-cargando">Cargando…</div>}
        </div>
      </section>

      {dialogo?.tipo === "formulario" && (
        <FormularioUsuario
          api={api}
          usuario={dialogo.usuario}
          esActual={esUsuarioActual(dialogo.usuario, actual)}
          onCerrar={cerrarDialogo}
          onCreado={(u, password) =>
            setDialogo({
              tipo: "password",
              usuario: u,
              password,
              titulo: "Usuario creado",
              mensaje: `El usuario ${u.nombre_usuario} fue creado correctamente.`,
            })
          }
          onModificado={() => {
            setDialogo(null);
            informar("Los datos del usuario se actualizaron correctamente.");
          }}
        />
      )}

      {dialogo?.tipo === "confirmar" && (
        <ConfirmarAccion
          api={api}
          accion={dialogo.accion}
          usuario={dialogo.usuario}
          onCerrar={cerrarDialogo}
          onListo={(mensaje, password) => {
            if (password) {
              setDialogo({
                tipo: "password",
                usuario: dialogo.usuario,
                password,
                titulo: "Contraseña restablecida",
                mensaje: `Se restableció la contraseña de ${dialogo.usuario.nombre_usuario}.`,
              });
            } else {
              setDialogo(null);
              informar(mensaje);
            }
          }}
        />
      )}

      {dialogo?.tipo === "password" && (
        <PasswordTemporal
          titulo={dialogo.titulo}
          usuario={dialogo.usuario}
          password={dialogo.password}
          onCerrar={() => {
            setDialogo(null);
            informar(dialogo.mensaje);
          }}
        />
      )}
    </>
  );
}

/** Si el usuario es el de la sesión. Sin sesión (modo dev) o en un alta nunca lo es. */
function esUsuarioActual(usuario: Usuario | null, actual: Usuario | null): boolean {
  return usuario !== null && actual !== null && usuario.id_usuario === actual.id_usuario;
}

function EstadoUsuario({ usuario }: { usuario: Usuario }) {
  if (!usuario.activo) return <span className="etiqueta etiqueta-baja">Dado de baja</span>;
  if (usuario.bloqueado) return <span className="etiqueta etiqueta-alerta">Bloqueado</span>;
  if (usuario.debe_cambiar_password) return <span className="etiqueta etiqueta-pendiente">Pendiente de ingreso</span>;
  return <span className="etiqueta etiqueta-activo">Activo</span>;
}

interface FormularioProps {
  api: GestionUsuariosApi;
  usuario: Usuario | null;
  esActual: boolean;
  onCerrar: () => void;
  onCreado: (usuario: Usuario, password: string) => void;
  onModificado: () => void;
}

function FormularioUsuario({ api, usuario, esActual, onCerrar, onCreado, onModificado }: FormularioProps) {
  const [datos, setDatos] = useState<UsuarioDatos>({
    nombre_usuario: usuario?.nombre_usuario ?? "",
    email: usuario?.email ?? "",
    nivel_acceso: (usuario?.nivel_acceso as Rol | null) ?? "CONSULTA",
  });
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setEnviando(true);
    try {
      if (usuario) {
        await api.modificar(usuario.id_usuario, datos);
        onModificado();
      } else {
        const r = await api.crear(datos);
        onCreado(r.usuario, r.password_temporal);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo={usuario ? "Modificar usuario" : "Nuevo usuario"}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button type="submit" form="form-usuario" className="boton boton-primario" disabled={enviando}>
            {enviando ? "Guardando…" : usuario ? "Guardar cambios" : "Crear usuario"}
          </button>
        </>
      }
    >
      <form id="form-usuario" onSubmit={enviar}>
        {error && <Alerta tipo="error">{error}</Alerta>}
        <label className="campo">
          <span>Nombre de usuario</span>
          <input
            value={datos.nombre_usuario}
            onChange={(e) => setDatos({ ...datos, nombre_usuario: e.target.value })}
            minLength={3}
            maxLength={100}
            required
            autoFocus
          />
        </label>
        <label className="campo">
          <span>Correo corporativo</span>
          <input
            type="email"
            value={datos.email}
            onChange={(e) => setDatos({ ...datos, email: e.target.value })}
            maxLength={255}
            required
          />
        </label>
        <label className="campo">
          <span>Perfil</span>
          <select
            value={datos.nivel_acceso}
            onChange={(e) => setDatos({ ...datos, nivel_acceso: e.target.value as Rol })}
            disabled={esActual}
          >
            {ROLES.map((r) => (
              <option key={r.valor} value={r.valor}>
                {r.etiqueta}
              </option>
            ))}
          </select>
          {esActual && <small className="texto-ayuda">No puede modificar su propio perfil.</small>}
        </label>
        {!usuario && (
          <p className="texto-ayuda">
            El sistema generará una contraseña temporal que el usuario deberá cambiar en su primer ingreso.
          </p>
        )}
      </form>
    </Modal>
  );
}

interface ConfirmarProps {
  api: GestionUsuariosApi;
  accion: Accion;
  usuario: Usuario;
  onCerrar: () => void;
  onListo: (mensaje: string, password?: string) => void;
}

function ConfirmarAccion({ api, accion, usuario, onCerrar, onListo }: ConfirmarProps) {
  const config = CONFIRMACIONES[accion];
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function confirmar() {
    setError(null);
    setEnviando(true);
    try {
      if (accion === "baja") {
        await api.darDeBaja(usuario.id_usuario);
        onListo(`El usuario ${usuario.nombre_usuario} fue dado de baja correctamente.`);
      } else if (accion === "reactivar") {
        await api.reactivar(usuario.id_usuario);
        onListo(`El usuario ${usuario.nombre_usuario} fue reactivado correctamente.`);
      } else if (api.restablecerPassword) {
        const r = await api.restablecerPassword(usuario.id_usuario);
        onListo("", r.password_temporal);
      }
    } catch (err) {
      setError(mensajeDeError(err));
      setEnviando(false);
    }
  }

  return (
    <Modal
      titulo={config.titulo}
      onCerrar={onCerrar}
      pie={
        <>
          <button type="button" className="boton boton-secundario" onClick={onCerrar}>
            Cancelar
          </button>
          <button
            type="button"
            className={`boton ${config.peligro ? "boton-peligro" : "boton-primario"}`}
            onClick={confirmar}
            disabled={enviando}
          >
            {enviando ? "Procesando…" : config.boton}
          </button>
        </>
      }
    >
      {error && <Alerta tipo="error">{error}</Alerta>}
      <p>
        <strong>{usuario.nombre_usuario}</strong> ({usuario.email})
      </p>
      <p className="texto-secundario">{config.texto}</p>
    </Modal>
  );
}

interface PasswordProps {
  titulo: string;
  usuario: Usuario;
  password: string;
  onCerrar: () => void;
}

function PasswordTemporal({ titulo, usuario, password, onCerrar }: PasswordProps) {
  const [copiado, setCopiado] = useState(false);

  async function copiar() {
    try {
      await navigator.clipboard.writeText(password);
      setCopiado(true);
    } catch {
      setCopiado(false);
    }
  }

  return (
    <Modal
      titulo={titulo}
      onCerrar={onCerrar}
      pie={
        <button type="button" className="boton boton-primario" onClick={onCerrar}>
          Entendido
        </button>
      }
    >
      <p>
        Contraseña temporal de <strong>{usuario.nombre_usuario}</strong> ({usuario.email}):
      </p>
      <div className="password-temporal">
        <code>{password}</code>
        <button type="button" className="boton boton-secundario boton-chico" onClick={copiar}>
          {copiado ? "Copiada" : "Copiar"}
        </button>
      </div>
      <Alerta tipo="aviso">
        Esta contraseña se muestra una sola vez. Entréguela al usuario por un medio seguro: deberá cambiarla en su
        primer ingreso.
      </Alerta>
    </Modal>
  );
}
