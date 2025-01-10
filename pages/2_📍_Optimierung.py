import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from pyomo.environ import *
import geopandas as gpd
import glpk

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Ein Projekt über Ladeinfrastruktur für Elektrofahrzeuge in Berlin
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "data/ladestation.png"
st.sidebar.image(logo)

# ---- Daten einlesen ----
@st.cache_data
def load_data():
    file_path = 'data/Ladesaeulenregister_Berlin_01122024.csv'
    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    df['Breitengrad'] = df['Breitengrad'].str.replace(',', '.').astype(float)
    df['Längengrad'] = df['Längengrad'].str.replace(',', '.').astype(float)
    df['Kosten'] = 10000  # Fiktive Kosten
    df['Abdeckung'] = 1   # Abdeckung pro Ladestation
    return df

@st.cache_data
def load_bezirke():
    url = 'https://raw.githubusercontent.com/funkeinteraktiv/Berlin-Geodaten/master/berlin_bezirke.csv'
    bezirke_df = pd.read_csv(url)
    return bezirke_df

ladesaeulen_df = load_data()
bezirke_df = load_bezirke()

# ---- Optimierungsmodell (Pyomo) ----
model = ConcreteModel()
model.x = Var(ladesaeulen_df.index, within=Binary)
model.obj = Objective(
    expr=sum(model.x[i] * ladesaeulen_df.loc[i, 'Kosten'] for i in ladesaeulen_df.index),
    sense=minimize
)
model.min_stations = Constraint(expr=sum(model.x[i] for i in ladesaeulen_df.index) >= 200)
model.coverage = Constraint(expr=sum(model.x[i] * ladesaeulen_df.loc[i, 'Abdeckung'] for i in ladesaeulen_df.index) >= 150)

solver = SolverFactory('glpk')
solver.solve(model)

selected_stations = [i for i in ladesaeulen_df.index if model.x[i]() == 1]

# ---- Streamlit App Layout ----
st.title("Ladeinfrastruktur in Berlin – Optimierung und Visualisierung")
st.sidebar.header("Filter Optionen")

# Filteroptionen in der Sidebar
betreiber_options = ['Alle'] + list(ladesaeulen_df['Betreiber'].unique())
selected_betreiber = st.sidebar.selectbox("Betreiber auswählen:", betreiber_options)

leistung_min, leistung_max = st.sidebar.slider(
    "Ladeleistung [kW] filtern:",
    int(ladesaeulen_df['Nennleistung Ladeeinrichtung [kW]'].min()),
    int(ladesaeulen_df['Nennleistung Ladeeinrichtung [kW]'].max()),
    (0, int(ladesaeulen_df['Nennleistung Ladeeinrichtung [kW]'].max()))
)

# Bezirksfilter
bezirk_options = ['Alle'] + list(bezirke_df['Gemeinde_name'].unique())
selected_bezirk = st.sidebar.selectbox("Bezirk auswählen:", bezirk_options)

# ---- Filter Logik ----
filtered_df = ladesaeulen_df[
    (ladesaeulen_df['Nennleistung Ladeeinrichtung [kW]'] >= leistung_min) &
    (ladesaeulen_df['Nennleistung Ladeeinrichtung [kW]'] <= leistung_max)
]

if selected_betreiber != 'Alle':
    filtered_df = filtered_df[filtered_df['Betreiber'] == selected_betreiber]

if selected_bezirk != 'Alle':
    bezirk_geometry = bezirke_df[bezirke_df['Gemeinde_name'] == selected_bezirk]
    bezirk_polygon = gpd.GeoSeries.from_wkt(bezirk_geometry['geometry']).unary_union
    filtered_df = filtered_df[
        filtered_df.apply(lambda x: bezirk_polygon.contains(Point(x['Längengrad'], x['Breitengrad'])), axis=1)
    ]

# ---- Karte erstellen ----
map_berlin = folium.Map(location=[52.5200, 13.4050], zoom_start=11)

# Bestehende Ladestationen (blau)
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Breitengrad'], row['Längengrad']],
        popup=(
            f"Bestehende Station<br>"
            f"Betreiber: {row['Betreiber']}<br>"
            f"Leistung: {row['Nennleistung Ladeeinrichtung [kW]']} kW<br>"
            f"Adresse: {row['Straße']} {row['Hausnummer']}"
        ),
        icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
    ).add_to(map_berlin)

# Optimierte Standorte (rot)
for i in selected_stations:
    row = ladesaeulen_df.iloc[i]
    folium.Marker(
        location=[row['Breitengrad'], row['Längengrad']],
        popup=(
            f"Optimierter Standort<br>"
            f"Betreiber: {row['Betreiber']}<br>"
            f"Leistung: {row['Nennleistung Ladeeinrichtung [kW]']} kW<br>"
            f"Adresse: {row['Straße']} {row['Hausnummer']}"
        ),
        icon=folium.Icon(color="red", icon="plus", prefix="fa")
    ).add_to(map_berlin)

# ---- Karte in der App anzeigen ----
folium_static(map_berlin)
