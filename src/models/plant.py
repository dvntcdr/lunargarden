from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from src.infra.db.base import Base


class SunlightType(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    DIRECT = 'direct'


class HealthStatus(StrEnum):
    HEALTHY = 'Healthy'
    ATTENTION = 'Needs attention'
    STRUGGLE = 'Struggling'
    DECEASED = 'Deceased'


class Plant(Base):
    __tablename__ = 'plants'

    name: Mapped[str] = mc(String(100), nullable=False)
    scientific_name: Mapped[str | None] = mc(String(200), nullable=True)
    common_name: Mapped[str | None] = mc(String(100), nullable=True)
    description: Mapped[str | None] = mc(Text, nullable=True)

    location: Mapped[str | None] = mc(String(100), nullable=True)
    pot_size: Mapped[str | None] = mc(String(50), nullable=True)
    soil_type: Mapped[str | None] = mc(String(100), nullable=True)

    # TODO: add image column

    acquired_date: Mapped[datetime | None] = mc(DateTime(timezone=True), nullable=True)

    health_status: Mapped[HealthStatus] = mc(Enum(HealthStatus), default=HealthStatus.HEALTHY, nullable=False)
    watering_frequency: Mapped[str | None] = mc(String(100), nullable=True)
    sunlight_type: Mapped[SunlightType] = mc(Enum(SunlightType), default=SunlightType.LOW, nullable=False)
    
    is_public: Mapped[bool] = mc(Boolean, default=True, nullable=False)
    is_favorite: Mapped[bool] = mc(Boolean, default=False, nullable=False)

    owner_id: Mapped[UUID] = mc(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='plants')
