from datetime import datetime, timedelta, timezone

from src.core.config import settings
from src.core.exceptions import (
	AlreadyExistsException,
	InvalidCredentialsException,
	TokenRevokedException,
	TokenExpiredException
)
from src.infra.security.auth import (
	create_access_token,
	create_refresh_token,
	hash_password,
	hash_refresh_token,
	verify_password,
)
from src.models.refresh_token import RefreshToken
from src.models.user import User
from src.repos.refresh_token import RefreshTokenRepository
from src.repos.user import UserRepository
from src.schemas.auth import TokenResponse
from src.schemas.user import UserCreate


class AuthService:

	def __init__(
		self,
		user_repo: UserRepository,
		token_repo: RefreshTokenRepository,
	) -> None:
		self.user_repo = user_repo
		self.token_repo = token_repo

	async def register(self, data: UserCreate) -> User:
		existing = await self.user_repo.get_by_username_or_email(
			username=data.username,
			email=data.email	
		)

		if existing is not None:
			raise AlreadyExistsException('User already exists')
		
		hashed_pwd = hash_password(data.password)

		user = User(
			username=data.username,
			email=data.email,
			full_name=data.full_name,
			password_hash=hashed_pwd
		)

		return await self.user_repo.create(user)
	
	async def login(self, username: str, password: str) -> TokenResponse:
		user = await self.user_repo.get_by_username(username)

		if user is None or not verify_password(password, user.password_hash):
			raise InvalidCredentialsException()
		
		# TODO: add if email is verified check

		return await self._generate_tokens(user)
	
	async def logout(self, refresh_token: str) -> None:
		token = await self._get_token(refresh_token)

		if token is None:
			raise InvalidCredentialsException()
		
		if token.is_revoked:
			raise TokenRevokedException()
		
		await self.token_repo.revoke(token)
	
	async def logout_all(self, user: User) -> None:
		await self.token_repo.revoke_all(user.id)
	
	async def refresh(self, raw_refresh: str, user: User) -> TokenResponse:
		token = await self._get_token(raw_refresh)

		if token is None:
			raise InvalidCredentialsException()
		
		if token.is_revoked:
			await self.token_repo.revoke_all(user.id)
			raise TokenRevokedException()
		
		if token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
			raise TokenExpiredException()

		await self.token_repo.revoke(token)

		return await self._generate_tokens(user)

	async def _generate_tokens(self, user: User) -> TokenResponse:
		access_token = create_access_token(payload={'sub': user.username})
		raw_refresh, hashed_refresh = create_refresh_token()

		refresh_token = RefreshToken(
			token_hash=hashed_refresh,
			expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
			owner_id=user.id
		)

		await self.token_repo.create(refresh_token)

		return TokenResponse(
			access_token=access_token,
			refresh_token=raw_refresh,
			expires_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS
		)
	
	async def _get_token(self, raw_token: str) -> RefreshToken | None:
		token_hash = hash_refresh_token(raw_token)
		return await self.token_repo.get_by_hash(token_hash)
