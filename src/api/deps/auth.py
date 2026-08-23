from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.deps.db.repos import TokenRepoDep, UserRepoDep
from src.core.config import settings
from src.services.auth import AuthService
from src.models.user import User
from src.infra.security.auth import verify_access_token
from src.core.exceptions import InvalidCredentialsException
from src.api.deps.db.repos import UserRepoDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.LOGIN_URL)


def get_auth_service(
    user_repo: UserRepoDep,
    token_repo: TokenRepoDep
) -> AuthService:
    return AuthService(user_repo, token_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
OAuth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    token: OAuth2SchemeDep,
    user_repo: UserRepoDep
) -> User:
    payload = verify_access_token(token)

    if payload is None:
        raise InvalidCredentialsException()
    
    username = payload.get('sub')

    if username is None:
        raise InvalidCredentialsException()
    
    user = await user_repo.get_by_username(username)

    if user is None:
        raise InvalidCredentialsException()

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
