import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors import ErrorNegocio
from app.routers import auth, usuarios

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("eugenia")

app = FastAPI(title="EugenIA API", version="0.1.0")
app.include_router(auth.router)
app.include_router(usuarios.router)


@app.exception_handler(ErrorNegocio)
def manejar_error_negocio(_: Request, exc: ErrorNegocio) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.mensaje})


@app.exception_handler(RequestValidationError)
def manejar_validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
    errores = [{"campo": ".".join(str(p) for p in e["loc"] if p != "body"), "mensaje": e["msg"]} for e in exc.errors()]
    detalle = "; ".join(f"{e['campo']}: {e['mensaje']}" for e in errores)
    return JSONResponse(status_code=422, content={"detail": f"Datos inválidos. {detalle}", "errores": errores})


@app.exception_handler(Exception)
def manejar_error_inesperado(request: Request, exc: Exception) -> JSONResponse:
    # CUU-018 *.a: se informa que no fue posible completar la operación y se registra el incidente.
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "No fue posible completar la operación."})


@app.get("/api/health", tags=["Salud"])
def health() -> dict[str, str]:
    # No consulta la base: Azure SQL serverless se pausa y el health check no debe mantenerla despierta.
    return {"estado": "ok"}
