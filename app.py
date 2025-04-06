import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📈 Dashboard de Criptomonedas - Datos de CoinGecko")

# Lista de algunas criptomonedas populares
coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Solana": "solana",
    "Dogecoin": "dogecoin"
}

coin_name = st.selectbox("Selecciona una criptomoneda", list(coins.keys()))
coin_id = coins[coin_name]

# Selección de días
days = st.slider("Cantidad de días a mostrar", min_value=1, max_value=90, value=30)

# Obtener datos de la API de CoinGecko
url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
params = {
    "vs_currency": "usd",
    "days": days
}
res = requests.get(url, params=params)
data = res.json()

# Procesar datos
prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit='ms')
volumes["timestamp"] = pd.to_datetime(volumes["timestamp"], unit='ms')

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Precio de {coin_name} (USD)")
    fig_price = px.line(prices, x="timestamp", y="price", title="Precio")
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader(f"Volumen de {coin_name}")
    fig_volume = px.area(volumes, x="timestamp", y="volume", title="Volumen")
    st.plotly_chart(fig_volume, use_container_width=True)
