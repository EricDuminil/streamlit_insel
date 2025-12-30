import insel
import streamlit as st
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

st.set_page_config(layout="wide", page_title="PV + Last + Batterie")
st.markdown(
    "<h1 style='text-align: center'>PV + Last + Batterie</h1>", unsafe_allow_html=True
)

left, right = st.columns([2, 3])

with left:
    st.header("Inputs")
    verbrauch = st.slider("🔌 Verbrauch", 1, 50, 10, format="%g MWh / a")
    pvleistung = st.slider("🌞 PV Leistung", 1, 50, 10, format="%g kWp")
    wirkungsgrad = st.slider("🦾 Batteriewirkungsgrad", 1, 100, 95, format="%g %%")
    kapazitaetbatterie = st.slider("🔋 Batteriekapazitaet", 0, 50, 5, format="%g kWh")

with right:
    st.header("Ergebnisse")
    right1, right2 = st.columns([2, 3])
    with right1:
        eigenverbrauchsquote, autarkiequote, cycles, last, ertrag, einspeisung, bezug  = insel.template(
            "Last_PV_Batterie.vseit",
            MWh_Verbrauch=verbrauch,
            kWp_PV=pvleistung,
            Kapazitaet_Batterie=kapazitaetbatterie,
            Wirkungsgrad_Batterie=wirkungsgrad / 100,
        )

        st.progress(
            eigenverbrauchsquote,
            text=f"🏠 Eigenverbrauchsquote = {eigenverbrauchsquote*100:.0f} %",
        )

        st.progress(
            autarkiequote,
            text=f"🏝️ Autarkiequote = {autarkiequote*100:.0f} %",
        )
    with right2:
        st.write("Just a test")
        x = np.linspace(0, 2*np.pi, 500)
        fig, ax = plt.subplots()
        # ax.plot(x, np.sin(x + verbrauch))
        # plt.savefig('templates/sin.png')
        # st.image("templates/sin.png")
        s = Sankey(ax=ax, unit=None)
        s.add(flows=[bezug, ertrag, -last, -einspeisung],
            labels=['Bezug', 'Ertrag', 'Verbrauch', 'Einspeisung'],
            orientations=[1,0, -1, -1])
        s.finish()
        st.pyplot(fig)

    st.badge(f"{cycles:.0f} Zyklen / a")
    st.subheader("Bezug")
    # NOTE: Could add a random id, for multi-users
    import time
    time.sleep(0.5)
    st.image("templates/last_pv_batterie.png")
