from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
