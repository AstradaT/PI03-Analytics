import pandas as pd
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from modules import get_historical_data


# Markets elegidos
coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'DOT', 'MATIC', 'TRX', 'AVAX']

coin = st.sidebar.selectbox(
    'Choose a Coin', coins)

st.title(f"Predict Future Price - {coin}")

df = get_historical_data(coin)
df = df[['date', 'close']]

df.columns = ["ds", "y"]
m = Prophet()
m.fit(df);
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)

st.plotly_chart(plot_plotly(m, forecast))