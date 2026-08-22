import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from pwdlib import PasswordHash

from src.core.config import settings

pwd_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
	return pwd_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
	return pwd_hash.verify(password, hash)


def create_access_token(payload: dict[str, Any]) -> str:
	to_encode = payload.copy()

	to_encode.update(
		{
			'exp': datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
			'iat': datetime.now(timezone.utc)
		}
	)

	return jwt.encode(
		to_encode,
		settings.SECRET_KEY,
		algorithm=settings.JWT_ALGORITHM
	)


def verify_access_token(token: str) -> dict | None:
	try:
		return jwt.decode(
			token, settings.SECRET_KEY, settings.JWT_ALGORITHM
		)
	except JWTError:
		return None


def create_refresh_token() -> tuple[str, str]:
	raw_token = secrets.token_urlsafe(64)
	token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

	return raw_token, token_hash


def hash_refresh_token(token: str) -> str:
	return hashlib.sha256(token.encode()).hexdigest()
