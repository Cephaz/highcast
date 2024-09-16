import json
import pytest
from datetime import datetime, timezone
from app.utils.export_utils import export_csv, export_json
from app import models

@pytest.fixture
def mock_consumption():
    return models.EnergyConsumption(
        id=1,
        consumption_kwh=100.5,
        datetime=datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc),
        zone="FR",
        carbon_intensity=50.0,
        carbon_footprint_kgco2e=5.025
    )

@pytest.mark.asyncio
async def test_export_csv(mock_consumption):
    response = export_csv([mock_consumption])

    assert response.media_type == "text/csv"
    assert response.headers["Content-Disposition"] == "attachment;filename=energy_consumption_export.csv"

    # Convert each string chunk to bytes before joining
    content = b''.join([chunk.encode() async for chunk in response.body_iterator]).decode()

    expected_header = "id,consumption_kwh,datetime,zone,carbon_intensity,carbon_footprint_kgco2e"
    expected_data = "1,100.5,2023-01-01T12:00:00+00:00,FR,50.0,5.025"

    assert expected_header in content
    assert expected_data in content

@pytest.mark.asyncio
async def test_export_json(mock_consumption):
    response = export_json([mock_consumption])
    
    assert response.media_type == "application/json"

    data = json.loads(response.body.decode())

    expected_data = [{
        "id": 1,
        "consumption_kwh": 100.5,
        "datetime": "2023-01-01T12:00:00+00:00",
        "zone": "FR",
        "carbon_intensity": 50.0,
        "carbon_footprint_kgco2e": 5.025
    }]

    assert data == expected_data
