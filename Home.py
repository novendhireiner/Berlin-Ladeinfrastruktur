import streamlit as st

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Ein Projekt über Ladeinfrastruktur für Elektrofahrzeuge in Berlin
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "data/ladestation.png"
st.sidebar.image(logo)

# Customize page title
st.title("Projekt - Ladeinfrastruktur für Elektrofahrzeuge in Berlin")

st.markdown(
    """
    Dieses Projekt zielt darauf ab, die Ladeinfrastruktur für Elektrofahrzeuge in Berlin zu analysieren und zu optimieren. Mithilfe von Geodaten, Verkehrsdaten und Optimierungsmodellen wird untersucht, wo neue Ladestationen platziert werden sollten, um eine maximale Abdeckung und Benutzerfreundlichkeit zu gewährleisten.

    Die interaktive Streamlit-Webanwendung visualisiert bestehende Ladestationen, analysiert die Nähe zu Verkehrsknotenpunkten und bietet Filtermöglichkeiten nach Betreiber, Ladeleistung und Bezirken. Optimierte Standorte für zukünftige Ladestationen werden auf der Karte hervorgehoben.
    """
)

st.header("Ziel des Projekts")

markdown = """
1. Optimierung der Standortauswahl für neue Ladestationen in Berlin.
2. Analyse bestehender Ladeinfrastruktur basierend auf aktuellen Daten.
3. Verkehrsflussanalyse mit OpenStreetMap (OSM)-Daten zur Identifizierung von Standorten mit hoher Fahrzeugdichte.
4. Interaktive Visualisierung von Ladestationen und Verkehrsknotenpunkten.
5. Erweiterte Filtermöglichkeiten zur Fokussierung auf bestimmte Betreiber, Ladeleistung oder Bezirke.
"""

st.markdown(markdown)

st.header("Hauptfunktionen der App")
st.markdown(
    """
    1. Visualisierung bestehender Ladestationen
        - Zeigt alle Ladestationen in Berlin auf einer interaktiven Karte.
        - Bestehende Ladestationen werden in blau dargestellt.
    2. Optimierungsmodell mit Pyomo
        - Optimiert die Standortauswahl für neue Ladestationen basierend auf:
            > Minimierung der Kosten für neue Installationen
            > Maximierung der Abdeckung von Verkehrsbereichen
        - Optimierte Standorte werden in rot angezeigt
    3. Verkehrsanalyse mit OpenStreeMap (OSM)
        - Lädt das Straßennetzwerk von Berlin und visualisiert es.
        - Bestehende Ladestationen entlang von Hauptverkehrsstraßen werden analysiert.
        - Ladestationen in der Nähe von Verkehrsknotenpunkten (innerhalb von 500 m) werden hervorgehoben.
    4. Filtermöglichkeiten
        - Betreiber: Filter nach bestimmten Ladestationsbetreibern.
        - Ladeleistung: Filter für minimale und maximale Ladeleistung.
        - Bezirk: Filter nach Berliner Bezirken.
        - Verkehrsanalyse: Zeigt Ladestationen entlang von Hauptstraßen und in der Nähe von Kreuzungen.
    """
)

st.header("Technologien und Tools")
st.markdown(
    """
    - Programmiersprachen: Python
    - Framework: Streamlit
    - Datenanalyse: Pandas, Geopandas
    - Optimierung: Pyomo
    - Geodaten: Folium, OSMnx (OpenStreetMap)
    - Kartenvisualisierung: Folium
    """
)

st.header("Datenquellen")
st.markdown(
    """
    1. Ladesäulenregister Berlin
        - CSV-Datei aus https://www.ladeinfrastruktur.berlin
    2. OpenStreetMap (OSM)
        - Straßennetzwerk von Berlin für die Verkehrsanalyse.
    3. Berliner Bezirksdaten:
        - CSV-Datei aus https://github.com/funkeinteraktiv/Berlin-Geodaten
    """
)

st.header("Beispielszenarien")
st.markdown(
    """
    Fall 1:
        - Zeige alle Ladestationen in Kreuzberg mit einer Ladeleistung von mindestens 50 kW.
    Fall 2:
        - Finde heraus, welche Ladestationen sich in der Nähe von Verkehrsknotenpunkten befinden, um den Bedarf für neue Stationen zu ermitteln.
    Fall 3:
        - Optimiere Standorte für 200 neue Ladestationen und visualisiere diese.
    """
)

st.header("Zukünftige Erweiterungen")
st.markdown(
    """
    - Heatmap-Analyse der Ladeinfrastruktur.
    - Simulation verschiedener Szenarien für schnelles oder langsames Wachstum der Elektromobilität.
    - Erweiterung auf andere Städte.
    """
)
