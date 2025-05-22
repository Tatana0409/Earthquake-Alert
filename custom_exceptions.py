class EarthquakeNotFoundException(Exception):
    def __init__(self, message="No earthquake data found"):
        super().__init__(message)