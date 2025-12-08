import insel
import streamlit as st

st.set_page_config(layout="wide")
st.title("INSEL online")

# TODO: Change title
# TODO: Change app name
# TODO: Results as table?
# TODO: Fix battery efficiency?

col1, col2 = st.columns([1, 1])
with col1:
    st.title("Bezug  💥👽👽👽👽👽 ")
    verbrauch = st.slider("🔌 Verbrauch [MWh/a]", 0, 50, 10)
    pvleistung = st.slider("🌞 PV Leistung [kWp]", 0, 50, 10)
    wirkungsgrad = st.slider("🔋 Batteriewirkungsgrad [%]", 0, 100, 95)
    kapazitaetbatterie = st.slider("🔋 Batteriekapazitaet [kWh]", 0, 50, 5)

with col2:
    eigenverbrauchsquote, autarkiequote = insel.template(
        "Last_PV_Batterie.vseit",
        MWh_Verbrauch=verbrauch,
        kWp_PV=pvleistung,
        Kapazitaet_Batterie=kapazitaetbatterie,
        Wirkungsgrad_Batterie=wirkungsgrad / 100,
    )

    st.write(f" Eigenverbrauchsquote = {round(eigenverbrauchsquote*100)} %")
    st.write(f" Autarkiequote 🗾 = {round(autarkiequote*100)} %")
    st.image("/tmp/Last_PV_Batterie.png")


# insel.template('sunorb.vseit', Longitude=lon, Latitude=lat, Timezone=timezone)
