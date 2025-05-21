import random
from earthguake_api_client import EarthquakeApiClient
import streamlit as st
import matplotlib.pyplot as plt
from earthquakes_filter import Earthquakes
from save_api_as_csv import SaveData
import folium
from streamlit_folium import st_folium
import matplotlib.ticker as ticker
import pandas as pd
from earthquake import Earthquake


# Initialize API client
client = EarthquakeApiClient(EarthquakeApiClient.api_url)
all_data = client.get_all_data()
filter = client.filter_by_type(client.e_type)
df = EarthquakeApiClient.convert_to_dataframe(filter)
# Create Earthquake instance with filtered data
earthquake_instance = Earthquakes({"features": filter})


# Retrieve query parameters
query_params = st.query_params
section = query_params.get("section", "home")

# Sidebar Navigation
st.sidebar.subheader("Navigation")
if st.sidebar.button("Welcome"):
    st.query_params["section"] = "home"
if st.sidebar.button("Earthquake Pager"):
    st.query_params["section"] = "pager"
if st.sidebar.button("Data Summary"):
    st.query_params["section"] = "data"
if st.sidebar.button("Map Visualization"):
    st.query_params["section"] = "map"
if st.sidebar.button("Top 10"):
    st.query_params["section"] = "top"
if st.sidebar.button("Save Data"):
    st.query_params["section"] = "save"
if st.sidebar.button("Reports"):
    st.query_params["section"] = "reports"

# Display section based on bookmarked query
if section == "home":
    st.subheader("👋 Hello!")



    st.markdown("""<style>.stApp { background-color: #FAEBD7; }.css-1d391kg { color: blue; }</style>""",
                unsafe_allow_html=True
                )

    st.title("Welcome to my first Python project :snake: ")
    st.markdown(
        """ 
           **:rainbow[This is my final Python course project.]**

           I prepared a Python application that fetches real-time earthquake data from the USGS API, 
           allows users to save and categorize events, and provides basic analysis and alert features.

           Features:
           - Fetch recent earthquake data from the past week in JSON format
           - Filter by magnitude, location, or time
           - Save and earthquake data locally as .csv
           - Simple analytics (e.g., strongest quake, count by region) 
           - Unit-tested core logic and components
           - Visual map plotting using `matplotlib`

           Hope you'll enjoy it

           Tatiana
           """
    )



elif section == "pager":
    st.subheader("⚠️ PAGER")

    st.write("Alert system for significant Earthquakes in last 7 days.")
    # Alert system
    data2 = earthquake_instance.filter_by_alert()
    df_alert = EarthquakeApiClient.convert_to_dataframe(data2)

    # Convert data into Earthquake objects
    earthquakes = [
        Earthquake(
            id=row["ID"],
            magnitude=row["Magnitude"],
            place=row["Place"],
            time=row["Time"],
            alert=row["Alert"],
            longitude=row["Longitude"],
            latitude=row["Latitude"]
        ) for _, row in df.iterrows()
    ]

    # Collect alerts from all earthquake instances
    alert_messages = []
    for eq in earthquakes:
        alert_msg = eq.pager()
        eq_cat = eq.category()
        if eq.alert in ["red", "yellow", "orange", "green"]:
            alert_messages.append((eq.alert, eq.place, alert_msg, eq_cat))

    # Display alert messages
    st.markdown(
        "<h3 style='color: red;'>Earthquake Pager</h3>",
        unsafe_allow_html=True
    )

    if alert_messages:
        for alert, place, message, category in alert_messages:
            if alert == "red":
                st.info(f"🔴 **Red Alert in {place}!** {message} Earthquake category: {category}.")
            elif alert == "orange":
                st.info(f"🟠 **Orange Alert in {place}:** {message} Earthquake category: {category}.")
            elif alert == "yellow":
                st.info(f"🟡 **Yellow Alert in {place}:** {message} Earthquake category: {category}.")
            elif alert == "green":
                st.info(f"🟢 **Green Alert in {place}:** {message} Earthquake category: {category}.")


            else:
                st.success("✅ No significant alerts. All recorded earthquakes this week are without alert level.")



elif section == "map":
    st.subheader("Map Visualization")

    st.title("Earthquake Map Visualization 🌍")
    # Ensure we have filtered data
    if not df.empty:
    # Center the map based on earthquake locations
        m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

    # Add markers for each earthquake
        for _, row in df.iterrows():
            folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Place']} | Magnitude: {row['Magnitude']}",
            icon=folium.Icon(color="red" if row["Magnitude"] > 5 else "orange")
            ).add_to(m)

    # Display the interactive map in Streamlit
        st_folium(m)  # Only initializes once
    else:
        st.warning("No earthquakes match the selected filters.")


elif section == "data":
    st.subheader("Data Summary")

    # Display all earthquakes data
    st.markdown(
    "<h3 style='color: red;'>All Earthquakes Data for the last 7 days:</h3>",
    unsafe_allow_html=True
    )
    st.write("Data Summary:")
    st.dataframe(df)  # Display raw data


elif section == "top":
    st.subheader("Strongest Earthquakes in last 7 days")

    # Top 10 places with strongest magnitude
    # Select top 10 strongest earthquakes by magnitude
    df_top_magnitude = df.nlargest(10, "Magnitude")

    # Extract relevant data
    top_places = df_top_magnitude[["Place", "Magnitude"]].sort_values(by="Magnitude", ascending=True)

    # Create horizontal bar chart
    st.subheader("Top 10 Places with Strongest Earthquakes")
    fig1, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_places["Place"], top_places["Magnitude"], color="firebrick")
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Place")
    ax.set_title("Top 10 Strongest Earthquake Locations")
    ax.invert_yaxis()  # Ensures strongest is at the top
    ax.bar_label(ax.containers[0], fmt="%.1f")  # Adds magnitude labels

    st.pyplot(fig1)



elif section == "save":
    st.subheader("Download All Earthquake data for last 7 days")
    # Save all data as csv via button
    st.markdown(
    "<h5 style='color: lightgreen;'>To download earthquake data from the USGS API for the last week in .csv format, just click the button below.</h3>",
    unsafe_allow_html=True
    )
    if st.button("Save all data as csv."):
        save = SaveData(EarthquakeApiClient.api_url)
        save.save_all_data()


else:
    st.subheader("📊 Reports Section")

    st.markdown(
    "<h1 style='color:green;'>Earthquake Data Visualization</h1>",
    unsafe_allow_html=True
    )

    # Filter by selected place

    # User selects a place from available earthquake locations
    available_places = df["Place"].dropna().unique().tolist()  # Remove NaN values

    # Extract text after "of", but keep locations without "of"
    split_places = [
        place.split("of", 1)[1].strip() if "of" in place else place
        for place in available_places
    ]

    # Ensure there are places to choose from
    if "selected_place" not in st.session_state:
        st.session_state["selected_place"] = random.choice(split_places) if split_places else "All"  # Fallback in case the list is empty

     # Dropdown for selecting location (default is the first randomly chosen place)
    default_index = split_places.index(st.session_state["selected_place"]) if st.session_state["selected_place"] in split_places else 0

    selected_place = st.selectbox(
        "Select Location:",
        ["All"] + split_places,
        index=(split_places.index(st.session_state["selected_place"]) + 1 if st.session_state[
                                                                                 "selected_place"] in split_places else 0),
        key="place_selector"  # Assign a unique key for proper state tracking
    )

    # Update session state when user makes a new selection
    if selected_place != st.session_state["selected_place"]:
        st.session_state["selected_place"] = selected_place

    # Apply filtering
    data = earthquake_instance.filter_by_place(st.session_state["selected_place"])
    df_place = client.convert_to_dataframe(data)



    # # User selects a place from available earthquake locations
    # available_places = df["Place"].dropna().unique().tolist()  # Remove NaN values
    #
    # # Extract text after "of" but keep locations that don't contain "of"
    # split_places = [
    # place.split("of", 1)[1].strip() if "of" in place else place
    # for place in available_places
    # ]
    # # Ensure there are places to choose from
    # if split_places:
    #     default_place = random.choice(split_places)  # Select a random place as default
    # else:
    #     default_place = "All"  # Fallback in case the list is empty
    #
    #
    # selected_place = st.selectbox("Select Location:", [default_place] + split_places)
    #
    # data = earthquake_instance.filter_by_place(selected_place)
    # df_place = client.convert_to_dataframe(data)

    # Handle case where no earthquakes match the filter
    if df_place.empty:
        st.warning("No earthquakes found for the selected location.")
    else:
    # Chart: Recorded Earthquakes near the selected location.
        st.subheader("Recorded Earthquakes near the selected location.")
        top_places = df_place["Place"].value_counts().nlargest(20)
        fig2, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_places.index, top_places.values, color="skyblue")
        ax.set_xlabel("Number of Earthquakes")
        # Ensure x-axis shows only integer ticks
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set_ylabel("Place")
        ax.set_title("Recorded Earthquakes near the selected location")
        ax.invert_yaxis()

        st.pyplot(fig2)


    #Filter by Magnitude

    st.markdown(
    "<h1 style='color:green;'>Earthquake Data Visualization</h1>",
    unsafe_allow_html=True
    )

    # User selects a minimum magnitude
    selected_magnitude = st.slider("Select Minimum Magnitude:", min_value=0.0, max_value=10.0, value=4.5, step=0.1)

    # Convert timestamp to readable date format
    df["Date"] = pd.to_datetime(df["Time"], unit='ms').dt.date

    # Ensure valid min/max dates for selection
    min_date, max_date = df["Date"].min(), df["Date"].max()
    start_date = st.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Select End Date", min_value=min_date, max_value=max_date, value=max_date)

    # Apply magnitude and date filtering
    filtered_data = earthquake_instance.filter_by_magnitude(selected_magnitude)
    df_filtered = client.convert_to_dataframe(filtered_data)
    df_filtered["Date"] = pd.to_datetime(df_filtered["Time"], unit='ms').dt.date
    df_filtered = df_filtered[(df_filtered["Date"] >= start_date) & (df_filtered["Date"] <= end_date)]

    # Ensure filtered dataset isn't empty
    if df_filtered.empty:
        st.warning("No earthquake data available for the selected filters.")
    else:
    # Display updated histogram
        st.subheader(f"Earthquake Magnitude Distribution (≥ {selected_magnitude}) from {start_date} to {end_date}")
        fig3, ax = plt.subplots()
        ax.hist(df_filtered["Magnitude"], bins=20, edgecolor="blue", color="skyblue")
        ax.set_xlabel("Magnitude")
        ax.set_ylabel("Frequency")
        ax.set_title("Filtered Earthquake Magnitude Distribution")
        st.pyplot(fig3)

    st.write(f"Showing earthquakes from {start_date} to {end_date}")











