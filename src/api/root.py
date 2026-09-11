from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.core.config import settings

router = APIRouter(tags=['root'])


@router.get('/')
async def root() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'service': settings.APP_NAME,
            'status': 'running',
            'version': settings.VERSION,
            'docs': [
                settings.DOCS_URL, settings.REDOC_URL
            ]
        }
    )
