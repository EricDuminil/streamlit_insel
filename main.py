import insel
import streamlit as st

st.set_page_config(layout="wide")
st.title("INSEL online")

col1, col2 = st.columns([1, 2])
with col1:
    lon = st.slider("Longitude", -180, 180, 30)
    lat = st.slider("Latitude", -90, 90, 30)

with col2:
    result = insel.block("SUM", lon, lat)
    st.write(f"{lon} + {lat} = {result}")


# insel.template('sunorb.vseit', Longitude=lon, Latitude=lat, Timezone=timezone)
# st.image("/tmp/sunorb.png")

