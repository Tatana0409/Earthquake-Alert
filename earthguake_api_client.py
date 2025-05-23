from typing import Any
import pandas as pd
import requests
from custom_exceptions import EarthquakeNotFoundException



class EarthquakeApiClient:
    api_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    # hour: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
    e_type = "earthquake"

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

    def filter_by_type(self, earthquake_type: str) -> list | None:
        # client = EarthquakeApiClient(self)
        # all_data = client.get_all_data()
        all_data = self.get_all_data()
        if not all_data or 'features' not in all_data:
            return []  # Handle missing data
        else:
            filtered_data = [feature for feature in all_data['features'] if
                             feature["properties"]["type"] == earthquake_type]
            # format_filtered_data = (json.dumps(filtered_data, indent=2))
            if not filtered_data:
                raise EarthquakeNotFoundException(
                    f'Data was not found while searching for its earthquake type {earthquake_type}!')
            return filtered_data

    @staticmethod
    def convert_to_dataframe(filtered_data):
        data = []
        for feature in filtered_data:
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {"coordinates": [None, None]})

            data.append({
                "Magnitude": properties.get("mag", None),
                "Place": properties.get("place", "Unknown"),
                "Time": properties.get("time", None),
                "Alert": properties.get("alert", None),
                "ID": properties.get("ids", None),
                "Latitude": geometry["coordinates"][1] if geometry["coordinates"] else None,
                "Longitude": geometry["coordinates"][0] if geometry["coordinates"] else None,
            })

        return pd.DataFrame(data)



# client = EarthquakeApiClient(EarthquakeApiClient.api_url)
# all_data = client.get_all_data()
# filter = client.filter_by_type(EarthquakeApiClient.e_type)
# df = EarthquakeApiClient.convert_to_dataframe(filter)
# print(df)



# Count Comparison
# print(f"Total items in all_data: {len(all_data['features']) if all_data else 0}")
# print(f"Total items in filtered_data: {len(filtered_data)}")
#
# # Key Comparison
# all_data_keys = {feature["id"] for feature in all_data['features']} if all_data else set()
# filtered_data_keys = {feature["id"] for feature in filtered_data}
# print(f"Keys in all_data but not in filtered_data: {all_data_keys - filtered_data_keys}")
# print(f"Keys in filtered_data but not in all_data: {filtered_data_keys - all_data_keys}")
