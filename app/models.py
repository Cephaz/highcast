from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .database import engine

Base = declarative_base()

class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    consumption_kwh = Column(Float, nullable=False)
    carbon_footprint_kgco2e = Column(Float)
    zone = Column(String(50), default="FR")

    def __repr__(self):
        return f"<EnergyConsumption(id={self.id}, timestamp={self.timestamp}, consumption_kwh={self.consumption_kwh}, carbon_footprint_kgco2e={self.carbon_footprint_kgco2e}, zone={self.zone})>"

Base.metadata.create_all(engine)
