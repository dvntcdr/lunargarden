from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps.db.repos import UserRepoDep, TokenRepoDep
from src.services.auth import AuthService


def get_auth_service(
    user_repo: UserRepoDep,
    token_repo: TokenRepoDep
) -> AuthService:
    return AuthService(user_repo, token_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
