import pytest
import csv
import os
from datetime import datetime
from save_api_as_csv import SaveData
from earthguake_api_client import EarthquakeApiClient
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_api_data():
    """Mock API data to simulate earthquake data retrieval"""
    return {
        "features": [
            {"properties": {"mag": 5.5, "place": "Tokyo", "alert": "red", "ids": "123"}},
            {"properties": {"mag": 3.1, "place": "California", "alert": "yellow", "ids": "456"}},
        ]
    }


@pytest.fixture
def save_data_instance(monkeypatch, mock_api_data):
    """Creates an instance of SaveData with mocked API response"""
    client = SaveData(EarthquakeApiClient.api_url)
    monkeypatch.setattr(client, "get_all_data", lambda: mock_api_data)
    return client


def test_save_all_data(save_data_instance):
    """Tests if data is correctly saved into a CSV file"""
    filename = f"earthquake_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Call the save method
    save_data_instance.save_all_data()

    # Verify file creation
    assert os.path.exists(filename), f"CSV file {filename} was not created"

    # Verify CSV content
    with open(filename, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert len(rows) == 2, "CSV file should contain 2 rows"
    assert rows[0]["place"] == "Tokyo", "First row should be Tokyo"
    assert rows[1]["place"] == "California", "Second row should be California"

    # Clean up - Delete test file
    os.remove(filename)


def test_save_data_error_handling(save_data_instance, monkeypatch, caplog):
    """Simulates a file writing failure and checks if the error is logged"""

    # Force an IOError when attempting to write the file
    monkeypatch.setattr("builtins.open",
                        lambda *args, **kwargs: (_ for _ in ()).throw(IOError("Simulated write error")))

    with caplog.at_level(logging.ERROR):
        save_data_instance.save_all_data()

    assert "Failed to write CSV file: Simulated write error" in caplog.text