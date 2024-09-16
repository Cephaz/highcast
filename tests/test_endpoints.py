from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch
from app.main import app
from app import schemas

client = TestClient(app)

def test_create_energy_consumption():
    with patch('app.carbon_calculator.add_energy_consumption') as mock_add:
        mock_add.return_value = schemas.EnergyConsumption(
            id=1,
            consumption_kwh=100,
            datetime=datetime.now(),
            zone="FR",
            carbon_intensity=100,
            carbon_footprint_kgco2e=10,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )

        response = client.post(
            "/consumption/",
            json={"consumption_kwh": 100, "datetime": datetime.now().isoformat(), "zone": "FR"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["consumption_kwh"] == 100
        assert data["zone"] == "FR"
        mock_add.assert_called_once()

def test_export_endpoint():
    response = client.get("/consumption/export/?format=json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    response = client.get("/consumption/export/?format=csv")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
