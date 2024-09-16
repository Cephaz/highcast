from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timedelta

class EnergyConsumptionBase(BaseModel):
    consumption_kwh: float = Field(..., gt=0)
    datetime: datetime
    zone: str = "FR"

class EnergyConsumptionCreate(EnergyConsumptionBase):
    pass

class EnergyConsumption(EnergyConsumptionBase):
    id: int
    carbon_intensity: float # gCO2eq/kWh
    carbon_footprint_kgco2e: float
    updated_at: datetime
    created_at: datetime

    ConfigDict(from_attributes=True)

class ExportParams(BaseModel):
    start_date: datetime = Field(default=datetime.now() - timedelta(days=7))
    end_date: datetime = Field(default=datetime.now())
    zone: str = Field(default="FR", description="Zone for which to export energy consumption data")
    format: Optional[str] = Field(default="json", pattern="^(csv|json)$", description="Export format: 'csv' or 'json'")
