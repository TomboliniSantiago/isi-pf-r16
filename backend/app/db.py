import logging
import time
from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

logger = logging.getLogger("eugenia.db")

# Azure SQL serverless pausada: responde 40613 ("not currently available") mientras se reanuda.
ERROR_BASE_REANUDANDOSE = "(40613)"


class Base(DeclarativeBase):
    pass


def conectar_con_reintentos(
    conectar: Callable[[], Any], intentos: int, espera: float, dormir: Callable[[float], None] = time.sleep
) -> Any:
    """Reintenta la conexión mientras la base se está reanudando; cualquier otro error se propaga."""
    for intento in range(1, intentos + 1):
        try:
            return conectar()
        except Exception as exc:
            if ERROR_BASE_REANUDANDOSE not in str(exc) or intento == intentos:
                raise
            logger.warning(
                "La base se está reanudando (intento %d de %d); se reintenta en %.0f s", intento, intentos, espera
            )
            dormir(espera)
    raise AssertionError("inalcanzable")


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    url = settings.sqlalchemy_url
    if not url.startswith("mssql"):
        return create_engine(url, pool_pre_ping=True)

    # El timeout de login de ODBC se pasa a pyodbc.connect(timeout=...): no es una clave válida de la cadena.
    engine = create_engine(
        url, pool_pre_ping=True, pool_recycle=1800, connect_args={"timeout": settings.db_connect_timeout}
    )

    @event.listens_for(engine, "do_connect")
    def _conectar(dialect, _conn_rec, cargs, cparams):
        return conectar_con_reintentos(
            lambda: dialect.loaded_dbapi.connect(*cargs, **cparams),
            intentos=settings.db_reanudacion_intentos,
            espera=settings.db_reanudacion_espera_segundos,
        )

    return engine


@lru_cache
def get_sessionmaker() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_db() -> Iterator[Session]:
    with get_sessionmaker()() as session:
        yield session
