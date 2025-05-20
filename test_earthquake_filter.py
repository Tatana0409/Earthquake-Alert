import pytest
from earthquakes_filter import Earthquakes
from custom_exceptions import EarthquakeNotFoundException


@pytest.fixture
def sample_earthquake_data():
    return {
        "features": [
            {"properties": {"mag": 4.5, "place": "California", "alert": "yellow"}},
            {"properties": {"mag": 5.2, "place": "Japan", "alert": "red"}},
            {"properties": {"mag": 2.8, "place": "Chile", "alert": None}},
        ]
    }


def test_filter_by_magnitude(sample_earthquake_data):
    eq = Earthquakes(sample_earthquake_data)
    result = eq.filter_by_magnitude(4.0)

    assert len(result) == 2  # Only California and Japan should be in results
    assert result[0]["properties"]["place"] == "California"
    assert result[1]["properties"]["place"] == "Japan"


def test_filter_by_magnitude_no_match(sample_earthquake_data):
    eq = Earthquakes(sample_earthquake_data)

    with pytest.raises(EarthquakeNotFoundException):
        eq.filter_by_magnitude(6.0)  # No earthquake above 6.0 exists


def test_filter_by_place(sample_earthquake_data):
    eq = Earthquakes(sample_earthquake_data)
    result = eq.filter_by_place("Japan")

    assert len(result) == 1
    assert result[0]["properties"]["place"] == "Japan"


def test_filter_by_place_no_match(sample_earthquake_data):
    eq = Earthquakes(sample_earthquake_data)

    with pytest.raises(EarthquakeNotFoundException):
        eq.filter_by_place("Atlantis")  # Atlantis doesn't exist


def test_filter_by_alert(sample_earthquake_data):
    eq = Earthquakes(sample_earthquake_data)
    result = eq.filter_by_alert()

    assert len(result) == 2  # Only California and Japan have alerts
    assert "yellow" in [quake["properties"]["alert"] for quake in result]
    assert "red" in [quake["properties"]["alert"] for quake in result]


def test_filter_by_alert_no_match():
    empty_data = {"features": []}
    eq = Earthquakes(empty_data)

    with pytest.raises(EarthquakeNotFoundException):
        eq.filter_by_alert()  # No earthquakes exist