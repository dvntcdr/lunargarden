import asyncio
import time

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.api.deps.db.session import SessionDep
from src.schemas.health import LivenessStatus, ReadynessStatus, Status

router = APIRouter(tags=['health'])


@router.get('/health/live', response_model=LivenessStatus)
async def liveness() -> LivenessStatus:
    return LivenessStatus(
        status=Status.OK,
        timestamp=time.time()
    )


async def check_db(session: AsyncSession) -> bool:
    try:
        await asyncio.wait_for(
            session.execute(text('SELECT 1')),
            timeout=2.0
        )
        return True
    except asyncio.TimeoutError:  # noqa
        return False


@router.get('/health/ready', response_model=ReadynessStatus)
async def readyness(session: SessionDep) -> JSONResponse:
    checks = {}

    db_ok = await check_db(session)
    checks['database'] = Status.OK if db_ok else Status.FAIL

    all_ok = all(value == Status.OK for value in checks.values())

    payload = ReadynessStatus(
        status='ready' if all_ok else 'not_ready',
        checks=checks
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=payload.model_dump()
    )
