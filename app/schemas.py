from pydantic import BaseModel
from datetime import datetime

class EnergyConsumptionBase(BaseModel):
    consumption_kwh: float
    zone: str = "FR"

class EnergyConsumptionCreate(EnergyConsumptionBase):
    pass

class EnergyConsumption(EnergyConsumptionBase):
    id: int
    timestamp: datetime
    carbon_footprint_kgco2e: float

    class Config:
        from_attributes = True

class EnergyConsumptionList(BaseModel):
    total: int
    items: list[EnergyConsumption]
