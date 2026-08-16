from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from src.core.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSession() as session:
        yield session
