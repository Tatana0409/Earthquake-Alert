from typing import Any
import pandas as pd
import csv
from datetime import datetime
from test import result


# Define the USGS Earthquake API
#USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# try:
#     df = pd.read_csv('all_month (1).csv')
#     print(df)
# except FileNotFoundError as e:
#         print('File was not found')

# read csv file to a list of dictionaries

class earthquake_data:

    def __int__(self, file_path:str)-> None:
        self.file_path = file_path


    def read_earthquake_data(self) -> None:
        try:
            df = pd.read_csv(self.file_path)
            print(df)
        except FileNotFoundError as e:
            print('File was not found')

    def csv_to_list_of_dic(self)-> list[dict[str | Any, str | Any]] | None:
        try:
            with open(self.file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                data = [row for row in csv_reader]
                return data
        except Exception as e:
            print('File was not found or convert to dict.')

print(earthquake_data.csv_to_list_of_dic('all_month (1).csv'))