import pytest
from earthguake_api_client import EarthquakeApiClient


@pytest.fixture
def mock_api_data():
    return {
        "features": [
            {"properties": {"mag": 5.5, "place": "Tokyo", "type": "earthquake", "alert": "red", "ids": "123"},
             "geometry": {"coordinates": [139.6917, 35.6895]}},
            {"properties": {"mag": 3.1, "place": "California", "type": "earthquake", "alert": "yellow", "ids": "456"},
             "geometry": {"coordinates": [-119.4179, 36.7783]}},
        ]
    }


def test_filter_by_type(mock_api_data, monkeypatch):
    client = EarthquakeApiClient(EarthquakeApiClient.api_url)

    monkeypatch.setattr(client, "get_all_data", lambda: mock_api_data)

    result = client.filter_by_type("earthquake")

    assert len(result) == 2
    assert result[0]["properties"]["place"] == "Tokyo"


def test_convert_to_dataframe(mock_api_data):
    df = EarthquakeApiClient.convert_to_dataframe(mock_api_data["features"])

    assert len(df) == 2
    assert "Magnitude" in df.columns
    assert "Place" in df.columns
    assert df.iloc[0]["Place"] == "Tokyo"