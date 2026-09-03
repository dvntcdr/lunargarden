from typing import Annotated

from fastapi import Depends

from src.api.deps.db.repos import PlantRepoDep
from src.services.plant import PlantService


def get_plant_service(plant_repo: PlantRepoDep) -> PlantService:
    return PlantService(plant_repo)


PlantServiceDep = Annotated[PlantService, Depends(get_plant_service)]
