from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
import csv
import io

from app import models

def export_csv(consumptions: List[models.EnergyConsumption]):
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['id', 'consumption_kwh', 'datetime', 'zone', 'carbon_intensity', 'carbon_footprint_kgco2e'])
    
    # Write data
    for consumption in consumptions:
        writer.writerow([
            consumption.id,
            consumption.consumption_kwh,
            consumption.datetime.isoformat(),
            consumption.zone,
            consumption.carbon_intensity,
            consumption.carbon_footprint_kgco2e
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=energy_consumption_export.csv"}
    )

def export_json(consumptions: List[models.EnergyConsumption]):
    data = [
        {
            "id": c.id,
            "consumption_kwh": c.consumption_kwh,
            "datetime": c.datetime.isoformat(),
            "zone": c.zone,
            "carbon_intensity": c.carbon_intensity,
            "carbon_footprint_kgco2e": c.carbon_footprint_kgco2e
        } for c in consumptions
    ]
    return JSONResponse(content=data)
