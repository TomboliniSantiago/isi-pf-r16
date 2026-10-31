from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de variables de entorno (o de backend/.env en desarrollo)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str | None = None
    db_host: str = "localhost"
    db_port: int = 1433
    db_name: str = "pfinalbasedd"
    db_user: str = ""
    db_password: str = ""
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_trust_cert: bool = False
    # Azure SQL serverless puede tardar en reanudarse tras una pausa automática.
    db_connect_timeout: int = 60

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    bcrypt_rounds: int = 12

    login_max_intentos: int = 3
    login_bloqueo_minutos: int = 15

    @property
    def sqlalchemy_url(self) -> str:
        if self.database_url:
            return self.database_url
        # Entre llaves para admitir ';' en la contraseña; '}' se escapa duplicándola.
        pwd = "{" + self.db_password.replace("}", "}}") + "}"
        odbc = (
            f"DRIVER={{{self.db_driver}}};SERVER=tcp:{self.db_host},{self.db_port};"
            f"DATABASE={self.db_name};UID={self.db_user};PWD={pwd};Encrypt=yes;"
            f"TrustServerCertificate={'yes' if self.db_trust_cert else 'no'}"
        )
        return "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)


@lru_cache
def get_settings() -> Settings:
    return Settings()
