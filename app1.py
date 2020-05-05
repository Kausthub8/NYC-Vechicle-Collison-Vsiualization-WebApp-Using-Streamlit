import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
DATA_URL = (
"/home/madhuri/Documents/nypd-motor-vehicle-collisions.csv"
)

st.title("Visualizing Vehicle Collisions in NYC")
st.markdown("Used for analyzing vehicle collisions in NYC")
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['ACCIDENT DATE', 'ACCIDENT TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'accident date_accident time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)


st.header("Where did most of the people get injured due to vehicle collisions in Nyc")
injured_people = st.slider("Number of people injured in vehicle collisons ", 0, 19)
st.map(data.query("@injured_people")[["latitude", "longitude"]].dropna(how="any", inplace=True))

st.header("How many collisions did occur during a time of day?");
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]


st.markdown("Vehicle Collision between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
   map_style="mapbox://styles/mapbox/light-v9",
   initial_view_state={
       "latitude": midpoint[0],
       "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
},
layers=[
    pdk.Layer(
    "HexagonLayer",
    data=data[['date/time', 'latitude', 'longitude']],
    get_position=['longitude', 'latitude'],
    radius=150,
    extruded=True,
    pickable=True,
    elevation_scale=4,
    elevation_range=[0, 1000],
    ),
],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered = data[
     (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=80, range=(0, 80))[0]
chart_data = pd.DataFrame({'minute': range(80), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=300)
st.write(fig)
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)





