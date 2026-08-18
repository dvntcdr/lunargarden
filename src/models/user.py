from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from src.infra.db.base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mc(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mc(String(200), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mc(String(200), nullable=True)
    password_hash: Mapped[str] = mc(String, nullable=False)
    is_active: Mapped[bool] = mc(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mc(Boolean, default=False, nullable=False)

    refresh_tokens = relationship('RefreshToken', back_populates='owner_id')
