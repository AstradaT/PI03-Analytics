import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, date, time, timedelta
from draw_candlestick import get_candlestick_plot


# Markets elegidos
coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'DOT', 'MATIC', 'TRX', 'AVAX']

coin = st.sidebar.selectbox(
    'Choose a Coin', coins)

st.title(f"{coin} to USD - Daily Chart")

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

# Get historical prices
@st.cache(allow_output_mutation=True)
def get_historical_data():
    resolution = 60 * 60 * 24
    url = f'https://ftx.com/api/markets/{coin}/USD/candles?resolution={resolution}'
    request = requests.get(url).json()
    df = pd.DataFrame(request['result'])
    df['date'] = pd.to_datetime(df['startTime']).dt.date
    df = df.drop(columns=['startTime', 'time'])
    return df

df = get_historical_data()

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
