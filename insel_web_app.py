import insel
import streamlit as st

st.set_page_config(layout="wide", page_title="PV + Last + Batterie")
st.markdown(
    "<h1 style='text-align: center'>PV + Last + Batterie</h1>", unsafe_allow_html=True
)
# TODO: Fix battery efficiency?

col1, col2 = st.columns([2, 3])
with col1:
    st.header("Inputs")
    verbrauch = st.slider("🔌 Verbrauch", 1, 50, 10, format="%g MWh / a")
    pvleistung = st.slider("🌞 PV Leistung", 1, 50, 10, format="%g kWp")
    wirkungsgrad = st.slider("🦾 Batteriewirkungsgrad", 1, 100, 95, format="%g %%")
    kapazitaetbatterie = st.slider("🔋 Batteriekapazitaet", 0, 50, 5, format="%g kWh")

with col2:
    st.header("Ergebnisse")
    eigenverbrauchsquote, autarkiequote = insel.template(
        "Last_PV_Batterie.vseit",
        MWh_Verbrauch=verbrauch,
        kWp_PV=pvleistung,
        Kapazitaet_Batterie=kapazitaetbatterie,
        Wirkungsgrad_Batterie=wirkungsgrad / 100,
    )

    autarkiequote = max(autarkiequote, 0)
    st.progress(
        eigenverbrauchsquote,
        text=f"🏠 Eigenverbrauchsquote = {eigenverbrauchsquote*100:.0f} %",
    )

    st.progress(
        autarkiequote,
        text=f"🏝️ Autarkiequote = {autarkiequote*100:.0f} %",
    )
    st.subheader("Bezug")
    st.image("/tmp/Last_PV_Batterie.png")


# insel.template('sunorb.vseit', Longitude=lon, Latitude=lat, Timezone=timezone)
