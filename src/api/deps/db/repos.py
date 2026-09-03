from typing import Annotated

from fastapi import Depends

from src.api.deps.db.session import SessionDep
from src.repos.plant import PlantRepository
from src.repos.refresh_token import RefreshTokenRepository
from src.repos.user import UserRepository


def get_user_repo(session: SessionDep) -> UserRepository:
	return UserRepository(session)


def get_token_repo(session: SessionDep) -> RefreshTokenRepository:
	return RefreshTokenRepository(session)


def get_plant_repo(session: SessionDep) -> PlantRepository:
	return PlantRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
TokenRepoDep = Annotated[RefreshTokenRepository, Depends(get_token_repo)]
PlantRepoDep = Annotated[PlantRepository, Depends(get_plant_repo)]
