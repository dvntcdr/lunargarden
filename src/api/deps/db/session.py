from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.infra.db.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
