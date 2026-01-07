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
    wirkungsgrad = (
        st.slider("🦾 Batteriewirkungsgrad", 1, 100, 95, format="%g %%") / 100
    )
    kapazitaetbatterie = st.select_slider(
        "🔋 Batteriekapazitaet",
        options=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000],
        value=10,
        format_func=lambda x: f"{x:g} kWh",
    )

    (
        eigenverbrauchsquote,
        autarkiequote,
        batterie_ladung,
        last,
        ertrag,
        einspeisung,
        bezug,
        batterie_entladung,
    ) = insel.template(
        "Last_PV_Batterie.vseit",
        MWh_Verbrauch=verbrauch,
        kWp_PV=pvleistung,
        Kapazitaet_Batterie=kapazitaetbatterie,
        Wirkungsgrad_Batterie=wirkungsgrad,
    )

    ########################
    #    Sankey diagram    #
    ########################

    # Nodes:
    #  PV:           0
    #  Bezug:        1
    #  Batterie:     2
    #  Verlust:      3
    #  Last:         4
    #  Verlust:      5
    #  Einspeisung:  6

    pv_to_battery = batterie_ladung
    verlust1 = pv_to_battery * (1 - wirkungsgrad) / wirkungsgrad
    battery_to_load = batterie_entladung * wirkungsgrad
    verlust2 = batterie_entladung * (1 - wirkungsgrad)
    pv_to_load = last - bezug - battery_to_load

    source = [
        0,
        0,
        0,
        1,
        0,
        2,
        2,
    ]
    target = [
        4,
        2,
        3,
        4,
        6,
        4,
        5,
    ]
    value = [
        pv_to_load,
        pv_to_battery,
        verlust1,
        bezug,
        einspeisung,
        battery_to_load,
        verlust2,
    ]
    link = dict(source=source, target=target, value=value)
    data = go.Sankey(
        link=link,
        arrangement="snap",
        node={
            "label": [
                "PV",
                "Bezug",
                "Battery",
                "Verlust",
                "Last",
                "Verlust",
                "Einspeisung",
            ],
            "x": [0.01, 0.01, 0.5, 0.5, 0.99, 0.99, 0.99],
            "y": [0.01, 0.99, 0.3, 0.3, 0.01, 0.01, 0.99],
            "color": [
                "#FFD700",  # PV (Yellow/Gold)
                "#808080",  # Bezug/Grid Import (Grey)
                "#2ECC71",  # Battery (Green)
                "#E74C3C",  # Verlust/Loss 1 (Red)
                "#3498DB",  # Last/Load (Blue)
                "#E74C3C",  # Verlust/Loss 2 (Red)
                "#F39C12",  # Einspeisung/Feed-in (Orange/Amber)
            ],
        },
    )
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
        if kapazitaetbatterie > 0:
            st.badge(f"{batterie_ladung / kapazitaetbatterie:.0f} Zyklen / a")
    st.subheader("Bezug")
    # NOTE: Could add a random id, for multi-users
    st.image("/tmp/Last_PV_Batterie.png")
