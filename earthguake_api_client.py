# res = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson')
from typing import Any
import requests
from custom_exceptions import EarthquakeNotFoundException


class EarthquakeApiClient:

    def __init__(self, api_path: str) -> None:
        self.api_path = api_path

    def get_all_data(self) -> bytes | None | Any:
        try:
            res = requests.get(self.api_path)
            res.raise_for_status()  # raise an exception for HTTP errors
            return res.json()  # convert response to dictionary

        except requests.exceptions.RequestException as e:
            print(f'Data was not gotten from API: {e}')
            return None

    def filter_by_type(self, earthquake_type: str) -> list[int | Any] | list | None:
        # client = EarthquakeApiClient(self)
        # all_data = client.get_all_data()
        all_data = self.get_all_data()
        if not all_data or 'features' not in all_data:
            return []  # Handle missing data
        else:
            filtered_data = [feature for feature in all_data["features"] if
                             feature["properties"]["type"] == earthquake_type]
            # format_filtered_data = (json.dumps(filtered_data, indent=2))
            if not filtered_data:
                raise EarthquakeNotFoundException(
                    f'Data was not found while searching for its earthquake type {earthquake_type}!')
            return filtered_data

client = EarthquakeApiClient('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson')
all_data = client.get_all_data()
filtered_data = client.filter_by_type('earthquake')

# Count Comparison
print(f"Total items in all_data: {len(all_data['features']) if all_data else 0}")
print(f"Total items in filtered_data: {len(filtered_data)}")

# Key Comparison
all_data_keys = {feature["id"] for feature in all_data["features"]} if all_data else set()
filtered_data_keys = {feature["id"] for feature in filtered_data}
print(f"Keys in all_data but not in filtered_data: {all_data_keys - filtered_data_keys}")
print(f"Keys in filtered_data but not in all_data: {filtered_data_keys - all_data_keys}")
