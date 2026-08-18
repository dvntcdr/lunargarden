from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from src.infra.db.base import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    token_hash: Mapped[str] = mc(String, unique=True, nullable=False, index=True)
    is_revoked: Mapped[bool] = mc(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mc(DateTime(timezone=True), nullable=False)

    owner_id: Mapped[UUID] = mc(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='refresh_tokens')
