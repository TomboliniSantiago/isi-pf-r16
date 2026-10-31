# EugenIA (ISI-PF-R16)

Sistema contable con OCR/NLP y validación con ARCA. Alcance y roadmap: [docs/alcance_70_y_roadmap_eugenia.md](docs/alcance_70_y_roadmap_eugenia.md).

| Carpeta | Contenido |
|---|---|
| `backend/` | API FastAPI + SQLAlchemy sobre SQL Server (Azure SQL) |
| `frontend/` | SPA React + Vite + TypeScript |
| `docs/` | Documentación funcional del proyecto |

## Casos de uso implementados

- **CUU-015 Iniciar sesión**: login con correo corporativo y contraseña (hash bcrypt), token JWT, bloqueo temporal tras 3 intentos fallidos consecutivos, cambio obligatorio de la contraseña temporal, cierre de sesión. 2FA y recuperación autónoma de contraseña quedan fuera de esta etapa (ver alcance).
- **CUU-018 Gestionar usuarios**: alta (con contraseña temporal generada por el sistema), modificación, consulta con filtros, baja lógica, reactivación y restablecimiento de contraseña. Solo el perfil Administrador accede.

Perfiles: `ADMINISTRADOR`, `CONTADOR`, `ADMINISTRATIVO`, `CONSULTA`. Los permisos se validan en el backend en cada request (una baja o un cambio de perfil tiene efecto inmediato).

Auditoría (`AUDITORIA_LOG`): `LOGIN_OK`, `LOGIN_FALLIDO`, `BLOQUEO`, `LOGOUT`, `CAMBIO_PASSWORD`, `ALTA`, `MODIFICACION`, `BAJA`, `REACTIVACION`, `RESTABLECER_PASSWORD`, con usuario, fecha (UTC), IP de origen y valores anteriores/nuevos. Nunca se registran contraseñas ni hashes.

## Puesta en marcha

### 1. Base de datos

Los scripts SQL (esquema base y migraciones) no se versionan en este repositorio. La base debe tener aplicada la migración `001_seguridad_usuarios.sql`, que agrega a `USUARIO` las columnas `intentos_fallidos`, `bloqueado_hasta`, `debe_cambiar_password`, `fecha_alta` y `ultimo_acceso`, índices únicos sobre `email` y `nombre_usuario`, y la columna `origen` a `AUDITORIA_LOG`.

Convenciones: `USUARIO.activo` = `'S'`/`'N'`; `USUARIO.email` en minúsculas.

### 2. Backend

Requiere Python 3.12 y el [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

```powershell
cd backend
copy .env.example .env                       # completar credenciales y JWT_SECRET
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt

.venv\Scripts\python -m app.cli crear-admin --email admin@empresa.com --nombre admin   # primer administrador
.venv\Scripts\python -m uvicorn app.main:app --reload                                   # http://localhost:8000/docs
```

Pruebas y lint (usan SQLite en memoria, no tocan la base real):

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ruff check .
```

### 3. Frontend

Requiere Node 20.

```powershell
cd frontend
npm install
npm run dev                   # http://localhost:5173 (redirige /api a localhost:8000)
npm run build                 # typecheck + build de producción
```
