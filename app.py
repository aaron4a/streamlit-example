import streamlit as st
import requests

@st.cache_data
def get_pokemon_list():
    r = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    if r.status_code == 200:
        return [p["name"] for p in r.json()["results"]]
    return []

@st.cache_data
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# 🌙 Tema oscuro
st.set_page_config(page_title="Pokédex Oscura", page_icon="🖤", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .css-1cpxqw2, .css-10trblm, .stTextInput > div > div > input,
    .stSelectbox, .stButton button {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border-radius: 10px;
    }
    .stMarkdown, .stSubheader {
        color: #ffffff !important;
    }
    .stProgress > div > div {
        background-color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌑 Pokédex en Modo Oscuro")

pokemon_list = get_pokemon_list()
pokemon_name = st.selectbox("Escribí o elegí un Pokémon:", pokemon_list)

if st.button("🔍 Buscar"):
    data = get_pokemon_data(pokemon_name)
    if data:
        st.image(data["sprites"]["other"]["official-artwork"]["front_default"], width=250)
        st.subheader(f"📛 Nombre: `{data['name'].capitalize()}`")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧬 Stats")
            for stat in data["stats"]:
                st.progress(min(stat["base_stat"] / 150, 1.0))
                st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")

        with col2:
            st.markdown("### 📘 Tipos")
            for t in data["types"]:
                st.success(f"🔹 {t['type']['name'].capitalize()}")

        st.markdown("### ⚔️ Movimientos principales")
        for move in data["moves"][:5]:
            st.code(move["move"]["name"])
    else:
        st.error("❌ Pokémon no encontrado.")
