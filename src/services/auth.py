from src.core.exceptions import AlreadyExists
from src.infra.security.auth import hash_password
from src.models.user import User
from src.repos.user import UserRepository
from src.schemas.user import UserCreate


class AuthService:
	def __init__(self, user_repo: UserRepository) -> None:
		self.user_repo = user_repo

	async def register(self, data: UserCreate) -> User:
		existing = await self.user_repo.get_by_username_or_email(
			username=data.username,
			email=data.email	
		)

		if existing is not None:
			raise AlreadyExists('User already exists')
		
		hashed_pwd = hash_password(data.password)

		user = User(
			username=data.username,
			email=data.email,
			full_name=data.full_name,
			password_hash=hashed_pwd
		)

		return await self.user_repo.create(user)
