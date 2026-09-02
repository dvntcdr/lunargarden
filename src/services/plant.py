from uuid import UUID

from src.core.exceptions import ForbiddenException, NotFoundException
from src.models.plant import Plant
from src.models.user import User
from src.repos.plant import PlantRepository
from src.schemas.plant import PlantCreate, PlantUpdate


class PlantService:

    def __init__(self, plant_repo: PlantRepository) -> None:
        self.plant_repo = plant_repo
    
    async def get_all(self, user: User) -> list[Plant]:
        return await self.plant_repo.get_all_by_owner(user.id)
    
    async def get_by_id(self, plant_id: UUID, user: User) -> Plant:
        return await self._get_plant_for_user(plant_id, user.id)
    
    async def _get_plant_for_user(self, plant_id: UUID, user_id: UUID) -> Plant:
        plant = await self.plant_repo.get_by_id(plant_id)

        if plant is None:
            raise NotFoundException('Plant not found')
        
        if plant.owner_id != user_id:
            raise ForbiddenException()

        return plant
    
    async def create(self, data: PlantCreate, user: User) -> Plant:
        plant = Plant(
            **data.model_dump(exclude_unset=True),
            owner_id=user.id
        )

        created = await self.plant_repo.create(plant)

        return created
    
    async def update(self, plant_id: UUID, data: PlantUpdate, user: User) -> Plant:
        plant = await self._get_plant_for_user(plant_id, user.id)
        updated = await self.plant_repo.update(plant, data.model_dump(exclude_unset=True))

        return updated
    
    async def delete(self, plant_id: UUID, user: User) -> None:
        plant = await self._get_plant_for_user(plant_id, user.id)
        await self.plant_repo.delete(plant)
