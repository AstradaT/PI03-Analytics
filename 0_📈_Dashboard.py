import streamlit as st
import pandas as pd
import numpy as np
import requests
from modules import get_candlestick_plot, get_historical_data


st.set_page_config(page_icon=':moneybag:', layout='wide')

# Markets elegidos
coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

coin = st.sidebar.selectbox(
    'Choose a Coin', coins)

col1, col2 = st.columns([1,8])
col1.image(f"img/{coin.lower()}.png", width=64)
col2.title(f"{coin} to USD - Daily Chart")

url = f'https://ftx.com/api/markets/{coin}/USD'
request = requests.get(url).json()
data = pd.Series(request['result'])

# Visualize coin data
col1, col2, col3 = st.columns(3)
col1.metric("Price", data['price'], f"{round(data['change24h']*100,2)}%")
col2.metric("Low 24h", data['priceLow24h'])
col3.metric("High 24h", data['priceHigh24h'])
val=int(data['volumeUsd24h'])
st.metric("Volume", f'{val:,}') # Volumen de transacciones

df = get_historical_data(coin)

# Draw candlestick chart
# Source: https://gist.github.com/GrovesD2/02477a448eaa94470f9572cd02b6d7ac#file-interactive_dash-py
days_to_plot = st.sidebar.slider(
    'Days to Plot', 
    min_value = 1,
    max_value = 300,
    value = 60,
)

ma1 = st.sidebar.number_input(
    'Moving Average #1 Length',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

ma2 = st.sidebar.number_input(
    'Moving Average #2 Length',
    value = 20,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

df[f'{ma1}_ma'] = df['close'].rolling(ma1).mean()
df[f'{ma2}_ma'] = df['close'].rolling(ma2).mean()
df = df[-days_to_plot:]

# Display the plotly chart on the dashboard
st.plotly_chart(
    get_candlestick_plot(df, ma1, ma2, coin),
    use_container_width = True,
)

variance = np.var(df['close'])
st.sidebar.metric("Variance", f'{variance:f}')
