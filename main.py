import insel
import streamlit as st

st.set_page_config(layout="wide")
st.title("INSEL online")

col1, col2 = st.columns([1, 1])
with col1:
    lon = st.slider("Longitude", -180, 180, 30)
    lat = st.slider("Latitude", -90, 90, 30)

with col2:
    result = insel.template("Last_PV_Batterie.vseit", x=lon, y=lat)
    st.write(f"{lon} + {lat} = {result}")
    st.image("/tmp/Last_PV_Batterie.png")


# insel.template('sunorb.vseit', Longitude=lon, Latitude=lat, Timezone=timezone)

