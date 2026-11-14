# EugenIA (ISI-PF-R16)

Backend FastAPI (`backend/`) y frontend React + Vite (`frontend/`) sobre SQL Server.

## Requisitos

- Python 3.12
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Node 20
- Base de datos con las migraciones `001` a `009` aplicadas en orden (se comparten fuera del repositorio)
- Opcional, para leer comprobantes en imagen o PDF escaneado: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) con el idioma español. Si no está en el PATH, indicar la ruta en `TESSERACT_CMD` del `.env`. Sin Tesseract, los PDF digitales se leen igual y las imágenes se completan a mano.

## Backend

```powershell
cd backend
copy .env.example .env      # completar base de datos y JWT_SECRET
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m app.cli crear-admin --email admin@empresa.com --nombre admin
```

Con `CORREO_MODO=consola` los códigos de verificación aparecen en la consola del backend en lugar de enviarse por correo.

## Frontend

```powershell
cd frontend
npm install
```

## Ejecutar

Doble clic en `iniciar.bat`: levanta backend (http://localhost:8000/docs) y frontend (http://localhost:5173). Al cerrar la ventana se detienen los dos.

## Pruebas

```powershell
cd backend
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ruff check .
```
