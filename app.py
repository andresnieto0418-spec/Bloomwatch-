import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Blooming Map", layout="wide")

st.title("🌸 Plant Blooming Interactive Map")
st.markdown("Explora especies endémicas y sus condiciones de floración en regiones seleccionadas.")

# Crear mapa base
m = folium.Map(location=[0, -60], zoom_start=3, tiles="CartoDB positron")

# Datos ficticios de especies por país
species_data = {
    "United States": {
        "name": "Sunflower",
        "scientific": "Helianthus annuus",
        "bloom": "Junio - Septiembre",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sunflower_sky_backdrop.jpg",
        "coords": [37.8, -96.9]
    },
    "Brazil": {
        "name": "Victoria Amazonica",
        "scientific": "Victoria amazonica",
        "bloom": "Diciembre - Marzo",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Victoria_amazonica_BotGardBln07122011B.jpg",
        "coords": [-3, -60]
    },
    "Colombia": {
        "name": "Orquídea",
        "scientific": "Cattleya trianae",
        "bloom": "Octubre - Enero",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Cattleya_trianae_Orchid.jpg",
        "coords": [4.5, -74]
    },
    "Peru": {
        "name": "Puya Raimondii",
        "scientific": "Puya raimondii",
        "bloom": "Cada 80-100 años (florece una sola vez)",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Puya_raimondii.jpg",
        "coords": [-10, -76]
    }
}

# Agregar marcadores con popups
for country, data in species_data.items():
    html = f"""
    <h4>{data['name']}</h4>
    <b>Nombre científico:</b> {data['scientific']}<br>
    <b>Floración:</b> {data['bloom']}<br>
    <img src="{data['image']}" width="200">
    """
    iframe = folium.IFrame(html=html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=300)
    folium.Marker(
        location=data["coords"],
        popup=popup,
        tooltip=country,
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)

# Mostrar mapa en Streamlit
st_data = st_folium(m, width=1200, height=600)
