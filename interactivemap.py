st.header("Where did most of the people get injured due to vehicle collisions in Nyc")
injured_people = st.slider("Number of people injured in vehicle collisons ", 0, 19)
st.map(data.query("@injured_people")[["latitude", "longitude"]].dropna(how="any", inplace=True))

st.header("How many collisions did occur during a time of day?");
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]


st.markdown("Vehicle Collision between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

