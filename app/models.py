from sqlalchemy import Column, Integer, Float, Date, DateTime, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .database import engine

Base = declarative_base()

class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, index=True)
    consumption_kwh = Column(Float, nullable=False)
    carbon_intensity = Column(Float, nullable=False)
    carbon_footprint_kgco2e = Column(Float, nullable=False)
    zone = Column(String(50), default="FR")
    datetime = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('zone', 'datetime', name='uq_zone_datetime'),
    )

    def __repr__(self):
        return f"<EnergyConsumption(id={self.id}, consumption_kwh={self.consumption_kwh}, carbon_intensity={self.carbon_intensity}, carbon_footprint_kgco2e={self.carbon_footprint_kgco2e}, zone={self.zone}, datetime={self.datetime}, updated_at={self.updated_at}, created_at={self.created_at})>"

Base.metadata.create_all(engine)