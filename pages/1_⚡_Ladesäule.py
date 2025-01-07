import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import osmnx as ox
from shapely.geometry import Point
import geopandas as gpd

st.set_page_config(layout="wide")


# ---- Streamlit Navigation ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite auswählen", ["Ladestation Visualisierung", "Verkehrsanalyse (OSM)"])

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
    return df

ladesaeulen_df = load_data()

# ---- Seite 1: Visualisierung der Ladestationen ----
if page == "Ladestation Visualisierung":
    st.title("Ladeinfrastruktur in Berlin")
    
    # Überprüfe auf fehlende Werte und filtere diese heraus
    valid_df = ladesaeulen_df.dropna(subset=['Breitengrad', 'Längengrad'])
    
    # Anzahl der entfernten Stationen anzeigen (falls vorhanden)
    #fehlende_koord = len(ladesaeulen_df) - len(valid_df)
    #if fehlende_koord > 0:
    #    st.warning(f"{fehlende_koord} Ladestationen wurden entfernt, da sie keine gültigen Koordinaten enthalten.")

    # Karte erstellen
    map_berlin = folium.Map(location=[52.5200, 13.4050], zoom_start=11)

    # Ladestationen auf der Karte anzeigen (blau)
    for _, row in valid_df.iterrows():
        folium.Marker(
            location=[row['Breitengrad'], row['Längengrad']],
            popup=(
                f"Betreiber: {row['Betreiber']}<br>"
                f"Leistung: {row['Nennleistung Ladeeinrichtung [kW]']} kW<br>"
                f"Adresse: {row['Straße']} {row['Hausnummer']}"
            ),
            icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
        ).add_to(map_berlin)
    
    # Karte anzeigen
    st_folium(map_berlin, width=2000, height=1000)

# ---- Seite 2: Verkehrsanalyse mit OSM ----
if page == "Verkehrsanalyse (OSM)":
    st.title("Verkehrsanalyse in Berlin mit OSM-Daten")

    @st.cache_data
    def load_osm_data():
        # Straßennetzwerk für Berlin von OpenStreetMap laden
        graph = ox.graph_from_place("Berlin, Germany", network_type="drive")
        nodes, edges = ox.graph_to_gdfs(graph)
        return nodes, edges

    nodes, edges = load_osm_data()

    # Straßennetz anzeigen
    st.subheader("Straßennetzwerk von Berlin")
    map_osm = folium.Map(location=[52.5200, 13.4050], zoom_start=11)

    # Straßen als Linien hinzufügen
    for _, edge in edges.iterrows():
        folium.PolyLine(
            locations=[(point[1], point[0]) for point in edge['geometry'].coords],
            color="gray",
            weight=1.5
        ).add_to(map_osm)
    
    # Ladesäulen auf der Karte anzeigen (blau)
    for _, row in ladesaeulen_df.iterrows():
        folium.Marker(
            location=[row['Breitengrad'], row['Längengrad']],
            popup=(f"Ladestation: {row['Betreiber']}"),
            icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
        ).add_to(map_osm)
    
    # Pufferzone von 500m um Knotenpunkte erstellen
    buffer = nodes.buffer(0.005)  # 0.005° ≈ 500m
    ladesaeulen_df['geometry'] = ladesaeulen_df.apply(lambda x: Point(x['Längengrad'], x['Breitengrad']), axis=1)
    gdf_ladesaeulen = gpd.GeoDataFrame(ladesaeulen_df, geometry='geometry', crs="EPSG:4326")
    nearby_ladesaeulen = gdf_ladesaeulen[gdf_ladesaeulen.intersects(buffer.unary_union)]

    # Markiere Ladesäulen in der Nähe von Verkehrsknotenpunkten (rot)
    for _, row in nearby_ladesaeulen.iterrows():
        folium.CircleMarker(
            location=[row['Breitengrad'], row['Längengrad']],
            radius=6,
            color="red",
            fill=True,
            fill_opacity=0.8,
            popup=f"In Nähe zu Verkehrsknoten: {row['Straße']}"
        ).add_to(map_osm)

    st_folium(map_osm, width=2000, height=1000)

    # Zusammenfassung der Ergebnisse
    st.subheader("Ergebnisse der Analyse")
    st.write(f"Anzahl der Ladestationen in der Nähe von Verkehrsknotenpunkten: {len(nearby_ladesaeulen)}")
