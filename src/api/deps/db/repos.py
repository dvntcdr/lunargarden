from typing import Annotated

from fastapi import Depends

from src.api.deps.db.session import SessionDep
from src.repos.refresh_token import RefreshTokenRepository
from src.repos.user import UserRepository


def get_user_repo(session: SessionDep) -> UserRepository:
	return UserRepository(session)


def get_token_repo(session: SessionDep) -> RefreshTokenRepository:
	return RefreshTokenRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
TokenRepoDep = Annotated[RefreshTokenRepository, Depends(get_token_repo)]
