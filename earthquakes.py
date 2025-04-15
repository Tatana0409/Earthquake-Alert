from earthquake import Earthquake
from custom_exceptions import EarthquakeNotFoundException

class Earthquakes:
    def __int__(self, earthquakes:list[Earthquake])-> None:
        self.earthquakes = earthquakes

    def all_categories(self):
        for earthquake in self.earthquakes:
            earthquake.category()

# Filter by magnitude
    def filter_earthquakes_by_magnitude(self, earthquake_magnitude:int) -> list[Earthquake]:
        matching_earthquakes = [e for e in self.earthquakes if e.magnitude == earthquake_magnitude]
        if not matching_earthquakes:
            raise EarthquakeNotFoundException(f'Earthquake was not found while searching for its magnitude! searched for: {earthquake_magnitude}')
        return matching_earthquakes

# Filter by location
    def filter_earthquakes_by_place (self, earthquake_place:str) -> list[Earthquake]:
        matching_earthquakes = [e for e in self.earthquakes if e.place == earthquake_place]
        if not matching_earthquakes:
            raise EarthquakeNotFoundException(f'Earthquake was not found while searching for its magnitude! searched for: {earthquake_place}')
        return matching_earthquakes

# Filter by time
    def filter_earthquakes_by_time (self, earthquake_time:str) -> list[Earthquake]:
        matching_earthquakes = [ e for e in self.earthquakes if e.time == earthquake_time]
        if not matching_earthquakes:
            raise EarthquakeNotFoundException(f'Earthquake was not found while searching for its magnitude! searched for: {earthquake_time}')
        return matching_earthquakes

#Strongest quake


#Count by reqion


