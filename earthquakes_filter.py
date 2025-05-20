from typing import List
from custom_exceptions import EarthquakeNotFoundException
from earthguake_api_client import EarthquakeApiClient
import re


class Earthquakes(EarthquakeApiClient):

    def __init__(self, earthquakes: dict):
        if not earthquakes or 'features' not in earthquakes:
            raise ValueError("Invalid or empty earthquake data provided.")
        self.earthquakes = earthquakes['features']


    def filter_by_magnitude(self, min_magnitude: float) -> List[dict]:
        filtered = [
            quake for quake in self.earthquakes
            if quake["properties"]["mag"] is not None and quake["properties"]["mag"] >= min_magnitude
         ]
        if not filtered:
            raise EarthquakeNotFoundException(f"No earthquakes found with magnitude >= {min_magnitude}")
        return filtered

    def filter_by_place(self, keyword: str) -> List[dict]:
        filtered = [
            quake
            for quake in self.earthquakes
            if re.search(f"{keyword}$", quake["properties"]["place"], re.IGNORECASE)  # Match places ending with the keyword
        ]
        if not filtered:
            raise EarthquakeNotFoundException(f"No earthquakes found in places containing '{keyword}'")
        return filtered

    def filter_by_alert(self) -> List[dict]:
        filtered = [
            quake
            for quake in self.earthquakes
            if quake["properties"]["alert"] is not None
        ]
        if not filtered:
            raise EarthquakeNotFoundException(f"No earthquakes found with alert.")
        return filtered

# #data = Earthquakes.filter_by_magnitude(EarthquakeApiClient.convert_to_dataframe(EarthquakeApiClient, filtered_data), 4.1)
# client = EarthquakeApiClient(EarthquakeApiClient.api_url)
# all_data = client.get_all_data()
# filtered_data = client.filter_by_type("earthquake")
# # Filter by magnitude
# data = earthquake_instance.filter_by_place("Texas$")
# df = EarthquakeApiClient.convert_to_dataframe(data)
#
# print(df)
#
# data1 = earthquake_instance.filter_by_magnitude(4.5)
# df1 = EarthquakeApiClient.convert_to_dataframe(data1)
# print(df1)
#
# alert = earthquake_instance.filter_by_alert()
# df3 = EarthquakeApiClient.convert_to_dataframe(alert)
# print(df3)
# # Create an instance of Earthquakes with filtered earthquake data
# earthquake_instance = Earthquakes({"features": filtered_data})

