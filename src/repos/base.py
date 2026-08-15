from typing import Any
from src.infra.db.session import AsyncSession
from sqlalchemy import select
from uuid import UUID


class BaseRepository[T]:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        if not hasattr(self, 'model'):
            raise NotImplementedError('Subclasses must define model')
        self.session = session

    async def get_all(self) -> list[T]:
        return list(
            await self.session.scalars(select(self.model))
        )
    
    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)
    
    async def create(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def update(self, instance: T, data: dict[str, Any]) -> T:
        await self.session.merge(instance)
        for field, value in data.items():
            setattr(instance, field, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, instance) -> None:
        await self.session.delete(instance)
        await self.session.commit()
