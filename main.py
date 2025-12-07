import insel
import streamlit as st

print("Hello from streamlit-insel!")

st.title("INSEL online")
lon = st.slider("Longitude", -180, 180, 30)
lat = st.slider("Latitude", -90, 90, 30)
result = insel.block("SUM", lon, lat)

# insel.template('sunorb.vseit', Longitude=lon, Latitude=lat, Timezone=timezone)
st.write(f"{lon} + {lat} = {result}")
print("Done")
# st.image("/tmp/sunorb.png")

