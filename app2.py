import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Blooming Map", layout="wide")
st.title("🌸 Plant Blooming Interactive Map")
st.markdown("Explora especies endémicas y sus condiciones de floración.")

# -----------------------------
# Datos ficticios
# -----------------------------
species_data = {
    "United States": [
        {
            "name": "Sunflower",
            "scientific": "Helianthus annuus",
            "bloom": "Junio - Septiembre",
            "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sunflower_sky_backdrop.jpg",
            "coords": [37.8, -96.9]
        },
        {
            "name": "Dogwood",
            "scientific": "Cornus florida",
            "bloom": "Abril - Mayo",
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Cornus_florida_flowers.jpg",
            "coords": [36, -80]
        }
    ],
    "Brazil": [
        {
            "name": "Victoria Amazonica",
            "scientific": "Victoria amazonica",
            "bloom": "Diciembre - Marzo",
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Victoria_amazonica_BotGardBln07122011B.jpg",
            "coords": [-3, -60]
        },
        {
            "name": "Ipê Amarillo",
            "scientific": "Handroanthus albus",
            "bloom": "Agosto - Septiembre",
            "image": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Ip%C3%AA_Amarelo_Brasilia.jpg",
            "coords": [-15.8, -47.9]
        }
    ],
    "Colombia": [
        {
            "name": "Orquídea",
            "scientific": "Cattleya trianae",
            "bloom": "Octubre - Enero",
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Cattleya_trianae_Orchid.jpg",
            "coords": [4.5, -74]
        },
        {
            "name": "Palma de cera",
            "scientific": "Ceroxylon quindiuense",
            "bloom": "Todo el año",
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/31/Ceroxylon_quindiuense_in_Cocora_Valley%2C_Colombia.jpg",
            "coords": [4.6, -75.5]
        }
    ],
    "Peru": [
        {
            "name": "Puya Raimondii",
            "scientific": "Puya raimondii",
            "bloom": "Cada 80-100 años",
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Puya_raimondii.jpg",
            "coords": [-10, -76]
        },
        {
            "name": "Cantuta",
            "scientific": "Cantua buxifolia",
            "bloom": "Primavera",
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/36/Cantua_buxifolia01.jpg",
            "coords": [-13.5, -72]
        }
    ]
}

# Coordenadas de los países (simplificadas)
country_coords = {
    "United States": [37.8, -96.9],
    "Brazil": [-10, -55],
    "Colombia": [4.5, -74],
    "Peru": [-9.2, -75]
}

# -----------------------------
# Interfaz
# -----------------------------
option = st.selectbox("Selecciona un país para explorar especies:", list(species_data.keys()))

# Crear mapa
m = folium.Map(location=country_coords[option], zoom_start=4, tiles="CartoDB positron")

# Añadir marcadores de especies del país seleccionado
for sp in species_data[option]:
    html = f"""
    <h4>{sp['name']}</h4>
    <b>Nombre científico:</b> {sp['scientific']}<br>
    <b>Floración:</b> {sp['bloom']}<br>
    <img src="{sp['image']}" width="200">
    """
    iframe = folium.IFrame(html=html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=300)
    folium.Marker(
        location=sp["coords"],
        popup=popup,
        tooltip=sp["name"],
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)

# Mostrar mapa en Streamlit
st_folium(m, width=1200, height=600)
