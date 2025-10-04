import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# --------------------------------
# CONFIGURACIÓN INICIAL DE LA APP
# --------------------------------
st.set_page_config(layout="wide", page_title="BloomWatch - Endemic Flowering Explorer")
st.title("🌸 Interactive Endemic Flowering Explorer")
st.write("Select a country by clicking on the map")

# --------------------------------
# DATOS DE EJEMPLO (se reemplazan después con los reales)
# --------------------------------
paises = {
    "United States": {
        "flag": "https://flagcdn.com/w320/us.png",
        "center": [37.0902, -95.7129],
        "zoom": 4,
        "species": [
            {
                "coords": [38.8977, -77.0365],
                "common": "Red Flower",
                "scientific": "Floralis rubra",
                "conditions": "Blooms in spring under moderate temperatures.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Red_flower.jpg/320px-Red_flower.jpg"
            },
            {
                "coords": [34.0522, -118.2437],
                "common": "Blue Flower",
                "scientific": "Floralis caerulea",
                "conditions": "Prefers arid climates and blooms in summer.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Blue_flower.jpg/320px-Blue_flower.jpg"
            }
        ]
    },
    "Brazil": {
        "flag": "https://flagcdn.com/w320/br.png",
        "center": [-14.235, -51.9253],
        "zoom": 4,
        "species": [
            {
                "coords": [-3.4653, -62.2159],
                "common": "Amazon Orchid",
                "scientific": "Cattleya violacea",
                "conditions": "Found in humid forests; blooms during the rainy season.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Cattleya_violacea_Orchid.jpg/320px-Cattleya_violacea_Orchid.jpg"
            },
            {
                "coords": [-15.7801, -47.9292],
                "common": "Yellow Ipe",
                "scientific": "Handroanthus albus",
                "conditions": "Blooms in the dry season of the Cerrado biome.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Yellow_Ipe_Tree.jpg/320px-Yellow_Ipe_Tree.jpg"
            }
        ]
    },
    "Colombia": {
        "flag": "https://flagcdn.com/w320/co.png",
        "center": [4.5709, -74.2973],
        "zoom": 5,
        "species": [
            {
                "coords": [4.711, -74.0721],
                "common": "May Flower",
                "scientific": "Cattleya trianae",
                "conditions": "Blooms between December and January in temperate climates.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Cattleya_trianae.jpg/320px-Cattleya_trianae.jpg"
            },
            {
                "coords": [6.2518, -75.5636],
                "common": "Heliconia",
                "scientific": "Heliconia rostrata",
                "conditions": "Prefers humid lowland rainforests.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Heliconia_rostrata2.jpg/320px-Heliconia_rostrata2.jpg"
            }
        ]
    },
    "Peru": {
        "flag": "https://flagcdn.com/w320/pe.png",
        "center": [-9.19, -75.0152],
        "zoom": 5,
        "species": [
            {
                "coords": [-13.532, -71.9675],
                "common": "Cantuta",
                "scientific": "Cantua buxifolia",
                "conditions": "Blooms in Andean highlands, especially in winter.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Cantua_buxifolia.jpg/320px-Cantua_buxifolia.jpg"
            },
            {
                "coords": [-12.0464, -77.0428],
                "common": "Amancaes Flower",
                "scientific": "Ismene amancaes",
                "conditions": "Blooms in coastal hills between June and August.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Flor_de_Amancaes.jpg/320px-Flor_de_Amancaes.jpg"
            }
        ]
    }
}

# --------------------------------
# CARGAR GEOJSON REDUCIDO
# --------------------------------
world = gpd.read_file("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json")

# Usar la columna correcta ("name") para filtrar
subset = world[world["name"].isin(paises.keys())]

# --------------------------------
# MAPA CONTINENTAL PRINCIPAL
# --------------------------------
m = folium.Map(location=[0, -60], zoom_start=3, tiles="CartoDB positron")

for _, row in subset.iterrows():
    pais = row["name"]
    folium.GeoJson(
        row["geometry"],
        name=pais,
        style_function=lambda x: {
            "color": "black",
            "weight": 1.2,
            "fillOpacity": 0.3,
            "fillColor": "white"
        },
        tooltip=f"Click to explore {pais}"
    ).add_to(m)

# Añadir banderas como overlay (simulado con ImageOverlay)
for p, data in paises.items():
    folium.raster_layers.ImageOverlay(
        image=data["flag"],
        bounds=[[data["center"][0]-10, data["center"][1]-15],
                [data["center"][0]+10, data["center"][1]+15]],
        opacity=0.4
    ).add_to(m)

# Mostrar mapa principal
st_map = st_folium(m, width=950, height=550)

# --------------------------------
# INTERACCIÓN CON PAÍSES
# --------------------------------
if st_map and st_map.get("last_object_clicked_tooltip"):
    pais_clic = st_map["last_object_clicked_tooltip"].replace("Click to explore ", "")
    if pais_clic in paises:
        st.success(f"You selected **{pais_clic}**")

        data = paises[pais_clic]
        m_country = folium.Map(location=data["center"], zoom_start=data["zoom"], tiles="CartoDB positron")

        for sp in data["species"]:
            popup_html = f"""
            <div style="width:250px">
                <h4>{sp['common']}</h4>
                <i>{sp['scientific']}</i>
                <p>{sp['conditions']}</p>
                <img src="{sp['photo']}" width="200px">
            </div>
            """
            folium.Marker(
                location=sp["coords"],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color="green", icon="leaf")
            ).add_to(m_country)

        st.write(f"### Endemic Species in {pais_clic}")
        st_folium(m_country, width=950, height=550)
