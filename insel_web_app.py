import insel
import plotly.graph_objects as go
import streamlit as st

# TODO: Avoid having to modify vseit or gnuplot between systems. Define an environment var, or use Pathlib

st.set_page_config(layout="wide", page_title="PV + Last + Batterie")
st.markdown(
    "<h1 style='text-align: center'>PV + Last + Batterie</h1>", unsafe_allow_html=True
)

left, right = st.columns([2, 2])

with left:
    st.header("Inputs")
    verbrauch = st.slider("🔌 Verbrauch", 1, 50, 10, format="%g MWh / a")
    pvleistung = st.slider("🌞 PV Leistung", 1, 50, 10, format="%g kWp")
    wirkungsgrad = st.slider("🦾 Batteriewirkungsgrad", 1, 100, 95, format="%g %%")
    kapazitaetbatterie = st.slider("🔋 Batteriekapazitaet", 0, 50, 5, format="%g kWh")

    eigenverbrauchsquote, autarkiequote, cycles, last, ertrag, einspeisung, bezug = (
        insel.template(
            "Last_PV_Batterie.vseit",
            MWh_Verbrauch=verbrauch,
            kWp_PV=pvleistung,
            Kapazitaet_Batterie=kapazitaetbatterie,
            Wirkungsgrad_Batterie=wirkungsgrad / 100,
        )
    )

    source = [0, 0, 1]
    target = [2, 3, 2]
    value = [ertrag - einspeisung, einspeisung, bezug]
    link = dict(source=source, target=target, value=value)
    data = go.Sankey(
        link=link,
        arrangement="snap",
        node={
            "label": ["PV", "Bezug", "Last", "Einspeisung"],
            "x": [0.01, 0.01, 0.99, 0.99],
            "y": [0.01, 0.99, 0.01, 0.99],
            "color": ["orange", "gray", "blue", "gray"]
        },
    )
    # TODO: Add battery
    # TODO: Check Battery 0kWh
    # FIXME: double text? https://discuss.streamlit.io/t/ghost-double-text-bug/68765/14
    fig = go.Figure(data)
    st.plotly_chart(fig)

with right:
    st.header("Ergebnisse")
    right1, right2 = st.columns([3, 2])
    with right1:

        st.progress(
            eigenverbrauchsquote,
            text=f"🏠 Eigenverbrauchsquote = {eigenverbrauchsquote*100:.0f} %",
        )

        st.progress(
            autarkiequote,
            text=f"🏝️ Autarkiequote = {autarkiequote*100:.0f} %",
        )

    with right2:
        st.badge(f"{cycles:.0f} Zyklen / a")
    st.subheader("Bezug")
    # NOTE: Could add a random id, for multi-users
    st.image("/tmp/Last_PV_Batterie.png")
