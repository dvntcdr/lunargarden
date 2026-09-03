from fastapi import APIRouter

from src.api.deps.auth import CurrentUserDep
from src.api.deps.domain.plant import PlantServiceDep
from src.models.plant import Plant
from src.schemas.plant import PlantResponse

router = APIRouter(prefix='/plants', tags=['Plants'])


@router.get('', response_model=list[PlantResponse])
async def get_plants(
    service: PlantServiceDep,
    current_user: CurrentUserDep
) -> list[Plant]:
    return await service.get_all(current_user)
