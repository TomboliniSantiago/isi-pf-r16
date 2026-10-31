from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    url = settings.sqlalchemy_url
    # El timeout de login de ODBC se pasa a pyodbc.connect(timeout=...): no es una clave válida de la cadena.
    connect_args = {"timeout": settings.db_connect_timeout} if url.startswith("mssql") else {}
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800, connect_args=connect_args)


@lru_cache
def get_sessionmaker() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_db() -> Iterator[Session]:
    with get_sessionmaker()() as session:
        yield session
