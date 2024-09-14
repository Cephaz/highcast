from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas, carbon_calculator
from .database import get_db

app = FastAPI()

@app.post("/consumption/", response_model=schemas.EnergyConsumption)
def create_energy_consumption(consumption: schemas.EnergyConsumptionCreate, db: Session = Depends(get_db)):
    return carbon_calculator.add_energy_consumption(
        db=db, 
        consumption_kwh=consumption.consumption_kwh,
        zone=consumption.zone
    )

@app.get("/consumption/", response_model=schemas.EnergyConsumptionList)
def read_energy_consumptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumptions = db.query(models.EnergyConsumption).offset(skip).limit(limit).all()
    total = db.query(models.EnergyConsumption).count()
    return {"total": total, "items": consumptions}

@app.get("/consumption/{consumption_id}", response_model=schemas.EnergyConsumption)
def read_energy_consumption(consumption_id: int, db: Session = Depends(get_db)):
    consumption = db.query(models.EnergyConsumption).filter(models.EnergyConsumption.id == consumption_id).first()
    if consumption is None:
        raise HTTPException(status_code=404, detail="Energy consumption not found")
    return consumption

@app.get("/total-carbon-footprint/")
def get_total_carbon_footprint(db: Session = Depends(get_db)):
    total = db.query(func.sum(models.EnergyConsumption.carbon_footprint_kgco2e)).scalar()
    return {"total_carbon_footprint_kgco2e": total or 0}