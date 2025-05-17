import streamlit as st
import requests

@st.cache_data
def get_pokemon_list():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    if response.status_code == 200:
        return [p["name"] for p in response.json()["results"]]
    return []

@st.cache_data
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# 🌟 Interfaz linda
st.set_page_config(page_title="Pokédex", page_icon="🧬", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎮 Pokédex Interactiva")

pokemon_list = get_pokemon_list()
pokemon_name = st.selectbox("Elegí o escribí un Pokémon:", pokemon_list, index=0)

if st.button("🔍 Buscar"):
    data = get_pokemon_data(pokemon_name)
    if data:
        st.image(data["sprites"]["other"]["official-artwork"]["front_default"], width=200)
        st.subheader(f"📛 Nombre: `{data['name'].capitalize()}`")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧬 Estadísticas")
            for stat in data["stats"]:
                st.progress(stat["base_stat"] / 150)
                st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")

        with col2:
            st.markdown("### 📘 Tipos")
            for t in data["types"]:
                st.info(f"✅ {t['type']['name'].capitalize()}")

        st.markdown("### ⚔️ Movimientos principales")
        for move in data["moves"][:5]:
            st.code(move["move"]["name"])
    else:
        st.error("❌ Pokémon no encontrado.")

