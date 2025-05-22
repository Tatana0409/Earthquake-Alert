import logging
logger = logging.getLogger(__name__)

class Earthquake:
    earthquake_count = 0

    def __init__(self, id:str, magnitude:int, place:str, time, alert:str, longitude: int, latitude: int)->None:
       self.id = id
       self.magnitude = magnitude
       self.place = place
       self.time = time
       self.alert = alert
       self.longitude = longitude
       self.latitude = latitude
       Earthquake.earthquake_count += 1

    def category(self) -> str:
        if self.magnitude <= 2.9:
            return "Mini"
        elif self.magnitude >= 3 and self.magnitude <= 3.9:
            return "Minor"
        elif self.magnitude >= 4 and self.magnitude <= 4.9:
            return "Light"
        elif self.magnitude >= 5 and self.magnitude <= 5.9:
            return "Moderate"
        elif self.magnitude >= 6 and self.magnitude <= 6.9:
            return "Strong"
        elif self.magnitude >= 7 and self.magnitude <= 7.9:
            return "Major"
        elif self.magnitude >= 8:
            return "Great"
        else:
            return "Category is not defined."

    def pager(self) -> str:
        alerts = {
            "green": "Low likelihood of casualties and damage.",
            "yellow": "Some damage is possible and the impact should be relatively localized.",
            "orange": "Significant damage is likely, and the disaster is potentially widespread.",
            "red": "Extensive damage is probable and the disaster is likely widespread."
        }
        return alerts.get(self.alert, "No earthquake alerts recorded.")