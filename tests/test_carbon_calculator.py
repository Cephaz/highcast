from unittest.mock import Mock, patch
from app import carbon_calculator
from datetime import datetime, timezone

def test_round_to_hour():
    dt = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
    rounded = carbon_calculator.round_to_hour(dt)
    assert rounded == "2023-01-01T13:00:00.00+00:00"

    dt = datetime(2023, 1, 1, 12, 29, 59, tzinfo=timezone.utc)
    rounded = carbon_calculator.round_to_hour(dt)
    assert rounded == "2023-01-01T12:00:00.00+00:00"

def test_add_energy_consumption():
    with patch('app.carbon_calculator.get_carbon_intensity', return_value=100):
        mock_session = Mock()

        result = carbon_calculator.add_energy_consumption(
            mock_session, 100, "2023-01-01T12:00:00.00+00:00", "FR"
        )

        assert result.consumption_kwh == 100
        assert result.zone == "FR"
        assert result.carbon_intensity == 100
        assert result.carbon_footprint_kgco2e == 10
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
