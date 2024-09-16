from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.utils.export_utils import export_csv, export_json

from . import models, schemas, carbon_calculator
from .database import get_db

app = FastAPI()

@app.post("/consumption/", response_model=schemas.EnergyConsumption)
def create_energy_consumption(
    consumption: schemas.EnergyConsumptionCreate, 
    db: Session = Depends(get_db)
):
    utc_datetime = consumption.datetime.astimezone(timezone.utc)
    formatted_datetime = carbon_calculator.round_to_hour(utc_datetime)

    return carbon_calculator.add_energy_consumption(
        db=db, 
        consumption_kwh=consumption.consumption_kwh,
        dt=formatted_datetime,
        zone=consumption.zone
    )

@app.get("/consumption/export/")
def export_energy_consumption(
    params: schemas.ExportParams = Depends(),
    db: Session = Depends(get_db)
):
    consumptions = db.query(models.EnergyConsumption).filter(
        and_(
            models.EnergyConsumption.datetime >= params.start_date,
            models.EnergyConsumption.datetime <= params.end_date,
            models.EnergyConsumption.zone == params.zone
        )
    ).all()

    if params.format == "csv":
        return export_csv(consumptions)
    else:
        return export_json(consumptions)
