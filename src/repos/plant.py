from uuid import UUID

from sqlalchemy import select, or_

from src.models.plant import Plant, HealthStatus, SunlightType
from src.repos.base import BaseRepository


class PlantRepository(BaseRepository[Plant]):
    model = Plant

    async def get_all_by_owner(self, user_id: UUID) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(Plant.owner_id == user_id)
        )
        return list(plants)
    
    async def get_all_by_owner_public(self, user_id: UUID) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(
                Plant.owner_id == user_id,
                Plant.is_public
            )
        )
        return list(plants)
    
    async def search_by_name(self, user_id: UUID, search_query: str) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(
                Plant.owner_id == user_id,
                or_(
                    Plant.name.icontains(search_query),
                    Plant.scientific_name.icontains(search_query),
                    Plant.common_name.icontains(search_query),
                )
            )
        )
        return list(plants)
    
    async def filter_by_health(self, user_id: UUID, health_status: HealthStatus) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(
                Plant.owner_id == user_id,
                Plant.health_status == health_status
            )
        )
        return list(plants)
    
    async def filter_by_sunlight(self, user_id: UUID, sunlight_type: SunlightType) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(
                Plant.owner_id == user_id,
                Plant.sunlight_type == sunlight_type
            )
        )
        return list(plants)
    
    async def get_favorites(self, user_id: UUID) -> list[Plant]:
        plants = await self.session.scalars(
            select(Plant).where(
                Plant.owner_id == user_id,
                Plant.is_favorite
            )
        )
        return list(plants)