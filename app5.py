import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Blooming Map", layout="wide")

st.title("🌸 Plant Blooming Interactive Map")
st.markdown("Explore endemic species and their blooming conditions in selected regions.")

# Crear mapa base
m = folium.Map(location=[0, -60], zoom_start=3, tiles="CartoDB positron")

# -------------------------------
# Datos de especies (2 por país)
# -------------------------------
species_data = {
    "United States": [
        {
            "name": "The Baldhip Rose",
            "scientific": "Rosa gymnocarpa",
            "bloom": "California — well-drained soils within forest understories.",
            "image": "https://i.postimg.cc/T3DLY9R7/20220425-112357-Copy-rotated.jpg",
            "coords": [38.5, -122.5]  # California (aprox)
        },
        {
            "name": "Quail Bush",
            "scientific": "Atriplex lentiformis",
            "bloom": "Arizona — dry climates with full sun and alkaline or saline soils.",
            "image": "https://i.postimg.cc/RFD4Hkdd/images-1.jpg",
            "coords": [33.4, -112.1]  # Arizona (aprox)
        }
    ],
    "Brazil": [
        {
            "name": "Red Maçaranduba",
            "scientific": "Brosimum rubescens",
            "bloom": "Amazon rainforest — humid, well-drained soils, 24–30°C.",
            "image": "https://i.postimg.cc/QddDfNz5/Whats-App-Image-2025-10-04-at-12-03-01-PM.jpg",
            "coords": [-3.0, -60.0]  # Amazon
        },
        {
            "name": "Brazil Nut Tree",
            "scientific": "Bertholletia excelsa",
            "bloom": "Amazon rainforest — deep, well-drained, slightly acidic soils, humid climate.",
            "image": "https://i.postimg.cc/BQM9P9vP/Whats-App-Image-2025-10-04-at-12-03-35-PM.jpg",
            "coords": [-6.5, -62.0]  # Amazon
        }
    ],
    "Colombia": [
        {
            "name": "May Flower Orchid",
            "scientific": "Cattleya trianae",
            "bloom": "Blooms Oct–Nov in rainy season; requires high humidity, indirect light, epiphytic bark support.",
            "image": "https://i.postimg.cc/762wSBRL/Whats-App-Image-2025-10-04-at-11-51-56-AM.jpg",
            "coords": [4.7, -74.0]  # Bogotá region
        },
        {
            "name": "Encenillo",
            "scientific": "Weinmannia acutifolia",
            "bloom": "Andean cloud forests, humid montane environments 2000–3500 m elevation.",
            "image": "https://i.postimg.cc/TYkFYVkW/imagen-2025-10-04-122937480.png",
            "coords": [5.0, -73.9]  # Andes region
        }
    ],
    "Peru": [
        {
            "name": "Puya raimondii (Queen of the Andes)",
            "scientific": "Puya raimondii",
            "bloom": "High-altitude puna grasslands (3000–4800 m), dry rocky soils under full sun.",
            "image": "https://i.postimg.cc/y6R8RdqX/imagen-2025-10-04-122715884.png",
            "coords": [-13.5, -71.9]  # Andes region
        },
        {
            "name": "Oxalis peruviana",
            "scientific": "Oxalis peruviana",
            "bloom": "High-altitude humid montane environments (700–3600 m).",
            "image": "https://i.postimg.cc/9FG06fJz/Whats-App-Image-2025-10-04-at-11-44-04-AM.jpg",
            "coords": [-12.0, -75.2]  # Andes region
        }
    ]
}

# -------------------------------
# Agregar marcadores al mapa
# -------------------------------
for country, species_list in species_data.items():
    for sp in species_list:
        html = f"""
        <h4>{sp['name']}</h4>
        <b>Scientific name:</b> {sp['scientific']}<br>
        <b>Blooming conditions:</b> {sp['bloom']}<br>
        <img src="{sp['image']}" width="200">
        """
        iframe = folium.IFrame(html=html, width=250, height=320)
        popup = folium.Popup(iframe, max_width=300)
        folium.Marker(
            location=sp["coords"],
            popup=popup,
            tooltip=f"{country}: {sp['name']}",
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(m)

# -------------------------------
# Mostrar mapa en Streamlit
# -------------------------------
st_data = st_folium(m, width=1200, height=600)
