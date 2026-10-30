from datetime import UTC, datetime


def ahora() -> datetime:
    """Fecha y hora UTC sin zona, que es como se persisten en la base."""
    return datetime.now(UTC).replace(tzinfo=None)


def a_utc(valor: datetime | None) -> datetime | None:
    """Marca como UTC una fecha leída de la base para serializarla sin ambigüedad."""
    return valor.replace(tzinfo=UTC) if valor else None
