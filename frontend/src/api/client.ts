const CLAVE_TOKEN = "eugenia.token";

export const tokenStore = {
  get(): string | null {
    try {
      return sessionStorage.getItem(CLAVE_TOKEN);
    } catch {
      return null;
    }
  },
  set(token: string): void {
    try {
      sessionStorage.setItem(CLAVE_TOKEN, token);
    } catch {
      /* almacenamiento no disponible: la sesión dura lo que la pestaña */
    }
  },
  clear(): void {
    try {
      sessionStorage.removeItem(CLAVE_TOKEN);
    } catch {
      /* idem */
    }
  },
};

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

let alExpirarSesion: (() => void) | null = null;

/** Registra qué hacer cuando el backend rechaza el token (sesión vencida o usuario dado de baja). */
export function onSesionExpirada(fn: () => void): void {
  alExpirarSesion = fn;
}

interface Opciones {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
}

export async function api<T>(ruta: string, { method = "GET", body }: Opciones = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: "application/json" };
  const token = tokenStore.get();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers["Content-Type"] = "application/json";

  let respuesta: Response;
  try {
    respuesta = await fetch(`/api${ruta}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError(0, "No fue posible conectarse con el servidor.");
  }

  if (respuesta.status === 204) return undefined as T;
  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    if (respuesta.status === 401 && token) alExpirarSesion?.();
    const mensaje = typeof datos?.detail === "string" ? datos.detail : "No fue posible completar la operación.";
    throw new ApiError(respuesta.status, mensaje);
  }
  return datos as T;
}

export function mensajeDeError(error: unknown): string {
  return error instanceof ApiError ? error.message : "No fue posible completar la operación.";
}
