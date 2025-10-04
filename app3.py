import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from branca.element import MacroElement, Template

# -------------------------------
# Configuración inicial de la app
# -------------------------------
st.set_page_config(layout="wide", page_title="Mapa de especies endémicas")
st.title("🌎 Herramienta interactiva de floración endémica")

# -------------------------------
# Datos de los países y banderas
# -------------------------------
paises = {
    "United States": {
        "flag": "https://flagcdn.com/w320/us.png",
        "center": [37.0902, -95.7129],
        "zoom": 4,
        "species": [
            {
                "coords": [38.8977, -77.0365],
                "common": "Flor Roja",
                "scientific": "Floralis rubra",
                "conditions": "Florece en primavera con temperaturas moderadas.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Red_flower.jpg/320px-Red_flower.jpg"
            },
            {
                "coords": [34.0522, -118.2437],
                "common": "Flor Azul",
                "scientific": "Floralis caerulea",
                "conditions": "Prefiere climas áridos y florece en verano.",
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
                "common": "Orquídea Amazónica",
                "scientific": "Cattleya violacea",
                "conditions": "Se encuentra en bosques húmedos y florece en temporada de lluvias.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Cattleya_violacea_Orchid.jpg/320px-Cattleya_violacea_Orchid.jpg"
            },
            {
                "coords": [-15.7801, -47.9292],
                "common": "Ipê Amarillo",
                "scientific": "Handroanthus albus",
                "conditions": "Florece durante la estación seca del Cerrado.",
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
                "common": "Flor de Mayo",
                "scientific": "Cattleya trianae",
                "conditions": "Florece entre diciembre y enero en climas templados.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Cattleya_trianae.jpg/320px-Cattleya_trianae.jpg"
            },
            {
                "coords": [6.2518, -75.5636],
                "common": "Heliconia",
                "scientific": "Heliconia rostrata",
                "conditions": "Prefiere zonas húmedas de selva baja.",
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
                "conditions": "Florece en la sierra andina, especialmente en invierno.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Cantua_buxifolia.jpg/320px-Cantua_buxifolia.jpg"
            },
            {
                "coords": [-12.0464, -77.0428],
                "common": "Flor de Amancaes",
                "scientific": "Ismene amancaes",
                "conditions": "Florece en las lomas costeras entre junio y agosto.",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Flor_de_Amancaes.jpg/320px-Flor_de_Amancaes.jpg"
            }
        ]
    }
}

# -------------------------------
# Ajuste de nombres (GeoJSON vs diccionario)
# -------------------------------
nombre_mapeo = {
    "United States of America": "United States",
    "Brazil": "Brazil",
    "Colombia": "Colombia",
    "Peru": "Peru"
}

# Cargar shapefile mundial desde GeoJSON externo
world = gpd.read_file("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json")

# Filtrar los países de interés
subset = world[world["name"].isin(nombre_mapeo.keys())]

# -------------------------------
# Crear mapa base
# -------------------------------
m = folium.Map(location=[10, -60], zoom_start=3)

# -------------------------------
# Insertar Leaflet.Pattern para texturas
# -------------------------------
pattern_template = """
{% macro script(this, kwargs) %}
    var imgPattern{{this.get_name()}} = new L.Pattern({{this.options|tojson}});
    var image = new L.PatternImage({url: '{{this.image_url}}', width: 200, height: 150});
    imgPattern{{this.get_name()}}.addShape(image);
    imgPattern{{this.get_name()}}.addTo(L.Patterns);
{% endmacro %}
"""

class ImagePattern(MacroElement):
    def __init__(self, image_url):
        super().__init__()
        self._name = "ImagePattern"
        self.image_url = image_url
        self._template = Template(pattern_template)
        self.options = {"width": 200, "height": 150}

# -------------------------------
# Dibujar los países con bandera
# -------------------------------
for _, row in subset.iterrows():
    nombre_geojson = row["name"]
    nombre_dict = nombre_mapeo[nombre_geojson]
    flag_url = paises[nombre_dict]["flag"]

    pattern = ImagePattern(flag_url)
    m.add_child(pattern)

    geojson = folium.GeoJson(
        row["geometry"],
        name=nombre_dict,
        style_function=lambda x, pat=pattern: {
            "color": "black",
            "weight": 1,
            "fillOpacity": 1,
            "fillPattern": pat.get_name()
        },
        tooltip=f"{nombre_dict} (clic para ver más)",
        highlight_function=lambda x: {"weight": 3, "color": "red"}
    )
    geojson.add_to(m)

st.write("### Selecciona un país haciendo clic en el mapa")
st_map = st_folium(m, width=900, height=600)

# -------------------------------
# Interacción: mapa de un país
# -------------------------------
if st_map and st_map.get("last_active_drawing"):
    props = st_map["last_active_drawing"].get("properties", {})
    pais_clic = props.get("name")

    if pais_clic and pais_clic in paises:
        st.success(f"Has seleccionado {pais_clic}")

        datos_pais = paises[pais_clic]

        # Crear mapa del país
        m_pais = folium.Map(location=datos_pais["center"], zoom_start=datos_pais["zoom"])

        # Añadir especies
        for especie in datos_pais["species"]:
            popup_html = f"""
            <div style="width:250px">
                <h4>{especie['common']}</h4>
                <p><i>{especie['scientific']}</i></p>
                <p>{especie['conditions']}</p>
                <img src="{especie['photo']}" width="200px">
            </div>
            """
            folium.Marker(
                location=especie["coords"],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color="green", icon="leaf")
            ).add_to(m_pais)

        st.write(f"### Especies endémicas en {pais_clic}")
        st_folium(m_pais, width=900, height=600)
