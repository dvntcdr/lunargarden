from enum import StrEnum

from pydantic import BaseModel

from src.core.config import settings


class Status(StrEnum):
    OK = 'ok'
    FAIL = 'fail'


class LivenessStatus(BaseModel):
    status: Status
    timestamp: float
    version: str = settings.VERSION
    app: str = settings.APP_NAME


class ReadynessStatus(BaseModel):
    status: str
    checks: dict[str, str]
