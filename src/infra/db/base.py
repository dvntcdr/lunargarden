from uuid import UUID as _UUID, uuid4
from datetime import datetime

from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base model class with common attrs
    """

    id: Mapped[_UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
