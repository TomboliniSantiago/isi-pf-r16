import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, OperationalError

from app.errors import ErrorNegocio
from app.routers import auth, dev_usuarios, plan_cuentas, usuarios

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("eugenia")

app = FastAPI(title="EugenIA API", version="0.1.0")
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(plan_cuentas.router)
app.include_router(dev_usuarios.router)  # sin inicio de sesión: solo para desarrollo


@app.exception_handler(ErrorNegocio)
def manejar_error_negocio(_: Request, exc: ErrorNegocio) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.mensaje})


@app.exception_handler(RequestValidationError)
def manejar_validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
    errores = [{"campo": ".".join(str(p) for p in e["loc"] if p != "body"), "mensaje": e["msg"]} for e in exc.errors()]
    detalle = "; ".join(f"{e['campo']}: {e['mensaje']}" for e in errores)
    return JSONResponse(status_code=422, content={"detail": f"Datos inválidos. {detalle}", "errores": errores})


def _base_no_disponible(exc: DBAPIError) -> bool:
    """Errores de conexión: red, credenciales o Azure SQL serverless reanudándose (40613).
    pyodbc no siempre los clasifica como OperationalError; se reconocen por SQLSTATE 08xxx."""
    if isinstance(exc, OperationalError):
        return True
    estado = exc.orig.args[0] if exc.orig is not None and exc.orig.args else ""
    return str(estado).startswith("08") or "(40613)" in str(exc.orig)


@app.exception_handler(DBAPIError)
def manejar_error_base(request: Request, exc: DBAPIError) -> JSONResponse:
    if "(40615)" in str(exc.orig):  # IP no habilitada en el firewall de Azure SQL
        logger.error("Firewall de Azure SQL rechazó la conexión: %s", exc.orig)
        return JSONResponse(
            status_code=503,
            content={
                "detail": "La base de datos rechazó la conexión: la IP no está habilitada en el firewall de Azure."
            },
        )
    if not _base_no_disponible(exc):
        return manejar_error_inesperado(request, exc)
    logger.error("Base de datos no disponible en %s %s: %s", request.method, request.url.path, exc.orig)
    return JSONResponse(
        status_code=503,
        content={"detail": "La base de datos no está disponible en este momento. Intente nuevamente en unos segundos."},
    )


@app.exception_handler(Exception)
def manejar_error_inesperado(request: Request, exc: Exception) -> JSONResponse:
    # CUU-018 *.a: se informa que no fue posible completar la operación y se registra el incidente.
    logger.error("Error no controlado en %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "No fue posible completar la operación."})


@app.get("/api/health", tags=["Salud"])
def health() -> dict[str, str]:
    # No consulta la base: Azure SQL serverless se pausa y el health check no debe mantenerla despierta.
    return {"estado": "ok"}
