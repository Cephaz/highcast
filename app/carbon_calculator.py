from datetime import datetime, timedelta, timezone
import requests
from sqlalchemy.orm import Session
from .models import EnergyConsumption
from . import config
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

G_TO_KG_CONVERSION = 1000


def round_to_hour(dt: datetime) -> str:
    """
    Rounds the given datetime to the nearest hour and returns it as an ISO 8601 string.
    
    Args:
        dt (datetime): The datetime to round.
    
    Returns:
        str: The rounded datetime as an ISO 8601 string.
    """
    if dt.minute >= 30:
        dt += timedelta(hours=1)
    rounded = dt.replace(minute=0, second=0, microsecond=0)
    
    return rounded.strftime('%Y-%m-%dT%H:00:00.00+00:00')


def get_carbon_intensity(zone: str = "FR") -> float:
    """
    Fetches the latest carbon intensity for a given zone from the Electricity Maps API.
    
    Args:
        zone (str): The geographical zone for which to fetch the carbon intensity. Defaults to "FR" (France).
    
    Returns:
        float: The carbon intensity in gCO2eq/kWh.
    
    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the response doesn't contain the expected data.
    """
    url = f"{config.ELECTRICITYMAPS_API_BASE_URL}/v3/carbon-intensity/latest"
    params = {"zone": zone}
    headers = {"auth-token": config.ELECTRICITYMAPS_API_KEY}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['carbonIntensity']
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to get carbon intensity: {str(e)}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid response from API: {str(e)}")


def calculate_carbon_footprint(consumption_kwh: float, carbon_intensity: float) -> float:
    """
    Calculates the carbon footprint in kgCO2e based on energy consumption and carbon intensity.
    
    Args:
        consumption_kwh (float): Energy consumption in kWh.
        carbon_intensity (float): Carbon intensity in gCO2eq/kWh.
    
    Returns:
        float: Carbon footprint in kgCO2e.
    """
    return (carbon_intensity * consumption_kwh) / G_TO_KG_CONVERSION

# TODO: Implement datetime-dependent API history retrieval
# Currently, dt takes the current time
def add_energy_consumption(db: Session, consumption_kwh: float, dt: datetime, zone: str = "FR"):
    """
    Adds a new energy consumption record to the database.

    Args:
        db (Session): SQLAlchemy database session.
        consumption_kwh (float): Energy consumption in kWh. Must be greater than 0.
        dt (datetime): Date and time of the energy consumption.
        zone (str, optional): Geographical zone for the energy consumption. Defaults to "FR" (France).

    Raises:
        HTTPException: 
            - If an energy consumption record already exists for the given hour and zone.
            - If consumption_kwh is 0 or negative.

    Returns:
        EnergyConsumption: The newly created energy consumption record.
    """
    if consumption_kwh <= 0:
        raise HTTPException(status_code=400, detail="Energy consumption must be greater than 0 kWh")

    carbon_intensity = get_carbon_intensity(zone)
    carbon_footprint = calculate_carbon_footprint(consumption_kwh, carbon_intensity)
    
    current_time = datetime.now(timezone.utc)

    new_consumption = EnergyConsumption(
        consumption_kwh=consumption_kwh,
        carbon_intensity=carbon_intensity,
        carbon_footprint_kgco2e=carbon_footprint,
        datetime=dt,
        zone=zone,
        updated_at=current_time,
        created_at=current_time
    )
    
    try:
        db.add(new_consumption)
        db.commit()
        db.refresh(new_consumption)
        return new_consumption
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="An energy consumption record already exists for this hour and zone")
