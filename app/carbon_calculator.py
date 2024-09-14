import requests
from sqlalchemy.orm import Session
from .models import EnergyConsumption
from . import config


G_TO_KG_CONVERSION = 1000

def get_carbon_intensity(zone: str = "FR"):
    """
    Fetches the latest carbon intensity for a given zone from the Electricity Maps API
    
    Args:
    zone (str): The geographical zone for which to fetch the carbon intensity
    
    Returns:
    float: The carbon intensity in gCO2eq/kWh
    
    Raises:
    requests.RequestException: If the API request fails
    ValueError: If the response doesn't contain the expected data
    """
    url = f"{config.ELECTRICITYMAPS_API_BASE_URL}/latest"
    params = {"zone": zone}
    headers = {"auth-token": config.ELECTRICITYMAPS_API_KEY}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data['carbonIntensity']
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to get carbon intensity: {str(e)}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid response from API: {str(e)}")


def calculate_carbon_footprint(consumption_kwh: float, zone: str = "FR") -> float:
    """
    Calculates the carbon footprint in kgCO2e based on energy consumption
    
    Args:
    consumption_kwh (float): Energy consumption in kWh
    zone (str): Geographical zone for carbon intensity
    
    Returns:
    float: Carbon footprint in kgCO2e
    """
    carbon_intensity = get_carbon_intensity(zone)
    return (carbon_intensity * consumption_kwh) / G_TO_KG_CONVERSION

def add_energy_consumption(db: Session, consumption_kwh: float, zone: str = "FR"):
    carbon_footprint = calculate_carbon_footprint(consumption_kwh, zone)
    new_consumption = EnergyConsumption(
        consumption_kwh=consumption_kwh,
        carbon_footprint_kgco2e=carbon_footprint,
    )
    db.add(new_consumption)
    db.commit()
    db.refresh(new_consumption)
    return new_consumption