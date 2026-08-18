from fastapi import APIRouter

from src.api.deps.auth import AuthServiceDep
from src.schemas.user import UserCreate, UserResponse
from src.models.user import User


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/signup', response_model=UserResponse)
async def register(service: AuthServiceDep, data: UserCreate) -> User:
    return await service.register(data)
