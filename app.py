import streamlit as st
import requests

st.title("🔍 Buscador de Pokémon")
pokemon_name = st.text_input("Escribí el nombre de un Pokémon:", "pikachu")

if st.button("Buscar"):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.header(data["name"].capitalize())
        st.image(data["sprites"]["front_default"])
        st.subheader("🧬 Stats:")
        for stat in data["stats"]:
            st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
        st.subheader("📘 Tipos:")
        types = [t["type"]["name"] for t in data["types"]]
        st.write(", ".join(types))
    else:
        st.error("❌ Pokémon no encontrado. Verificá el nombre.")

