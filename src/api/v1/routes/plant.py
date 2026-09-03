from uuid import UUID

from fastapi import APIRouter, status

from src.api.deps.auth import CurrentUserDep
from src.api.deps.domain.plant import PlantServiceDep
from src.models.plant import Plant
from src.schemas.plant import PlantCreate, PlantResponse, PlantUpdate

router = APIRouter(prefix='/plants', tags=['Plants'])


@router.get('/', response_model=list[PlantResponse])
async def get_plants(
    service: PlantServiceDep,
    current_user: CurrentUserDep
) -> list[Plant]:
    return await service.get_all(current_user)


@router.post('/', response_model=PlantResponse)
async def create_plant(
    service: PlantServiceDep,
    data: PlantCreate,
    current_user: CurrentUserDep
) -> Plant:
    return await service.create(data, current_user)


@router.patch('/{plant_id}', response_model=PlantResponse)
async def update_plant(
    service: PlantServiceDep,
    plant_id: UUID,
    data: PlantUpdate,
    current_user: CurrentUserDep
) -> Plant:
    return await service.update(plant_id, data, current_user )


@router.delete('/{plant_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(
    service: PlantServiceDep,
    plant_id: UUID,
    current_user: CurrentUserDep
) -> None:
    return await service.delete(plant_id, current_user)
