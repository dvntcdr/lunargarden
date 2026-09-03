from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from src.models.plant import HealthStatus, SunlightType


class PlantBase(BaseModel):
    scientific_name: str | None = Field(None, max_length=100)
    common_name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    location: str | None = Field(None, max_length=100)
    pot_size: str | None = Field(None, max_length=100)
    soil_type: str | None = Field(None, max_length=100)
    acquired_date: datetime | None = None
    health_status: HealthStatus = HealthStatus.HEALTHY
    watering_frequency: str | None = Field(None, max_length=200)
    sunlight_type: SunlightType = SunlightType.LOW


class PlantCreate(PlantBase):
    name: str = Field(..., min_length=1, max_length=100)
    

class PlantUpdate(PlantBase):
    name: str | None = Field(None, min_length=1, max_length=100)    


class PlantResponse(BaseModel):
    id: UUID

    name: str
    scientific_name: str | None
    common_name: str | None
    description: str | None
    location: str | None
    pot_size: str | None
    soil_type: str | None
    acquired_date: datetime | None
    health_status: HealthStatus
    watering_frequency: str | None
    sunlight_type: SunlightType

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
