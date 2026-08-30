from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.version import __version__


class Settings(BaseSettings):

    APP_NAME: str = 'LunarGarden'
    DESCRIPTION: str = 'The API for Plant Parents.'
    VERSION: str = __version__
    DOCS_URL: str = '/docs'
    REDOC_URL: str = '/redoc'

    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str
    
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600
    JWT_ALGORITHM: str = 'HS256'
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str
    
    LOGIN_URL: str = '/v1/auth/token'

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            'title': self.APP_NAME,
            'description': self.DESCRIPTION,
            'version': self.VERSION,
            'docs_url': self.DOCS_URL,
            'redoc_url': self.REDOC_URL,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
