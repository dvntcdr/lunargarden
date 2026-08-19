from uuid import UUID

from sqlalchemy import select

from src.models.refresh_token import RefreshToken
from src.repos.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    async def get_by_hash(self, hash: str) -> RefreshToken | None:
        return await self.session.scalar(
            select(RefreshToken).where(RefreshToken.token_hash == hash)
        )
    
    async def revoke(self, token: RefreshToken) -> None:
        token.is_revoked = True
        await self.session.commit()
    
    async def revoke_all(self, user_id: UUID) -> None:
        tokens = await self.session.scalars(
            select(RefreshToken).where(RefreshToken.owner_id == user_id)
        )

        for token in tokens.all():
            token.is_revoked = True
        
        await self.session.commit()
