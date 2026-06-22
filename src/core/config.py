from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.version import __version__
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings class
    """

    APP_NAME: str = 'LunarGarden'
    DESCRIPTION: str = 'Application for plants lovers.'
    VERSION: str = __version__

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
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
