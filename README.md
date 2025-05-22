# Earthquake-Alert
Earthquake Alert & Analysis App

A Python application that fetches real-time earthquake data from the USGS API, allows users to save and categorize events, and provides basic analysis and alert features.
## Features
- Fetch recent earthquake data from the past week in JSON format
- Filter by magnitude, location, or time
- Save and earthquake data locally as .csv
- Simple analytics (e.g., strongest quake, count by region)
- Alert system for significant earthquakes
- Unit-tested core logic and components
- Visual map plotting using matplotlib

You can run the application in two ways:
1. In Bowser mode: with the command in the terminal: streamlit run main.py
2. In desktop mode: just run run_app.py

The below libraries are required:
- re
- typing
- pytest
- pandas
- requests
- csv
- datetime
- logging
- random
- streamlit
- matplotlib.pyplot
- matplotlib.ticker
- folium
- streamlit_folium
- webview ( instead 'pip install webview' use 'pip install pywebview')

Kindly note:
If you noticed that nothing happened after clicking, click again :)

