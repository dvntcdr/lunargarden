from fastapi import APIRouter, status

from src.api.deps.auth import AuthServiceDep, LoginFormDep, CurrentUserDep
from src.schemas.auth import TokenResponse, RefreshRequest
from src.schemas.user import UserCreate, UserResponse
from src.models.user import User


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/signup', response_model=UserResponse)
async def register(service: AuthServiceDep, data: UserCreate) -> User:
    return await service.register(data)


@router.post('/token', response_model=TokenResponse)
async def login(service: AuthServiceDep, form_data: LoginFormDep) -> TokenResponse:
    return await service.login(form_data.username, form_data.password)


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    service: AuthServiceDep,
    data: RefreshRequest,
    current_user: CurrentUserDep  # noqa
) -> None:
    return await service.logout(data.refresh_token)


@router.post('/logout-all', status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    service: AuthServiceDep,
    current_user: CurrentUserDep
) -> None:
    return await service.logout_all(current_user)
