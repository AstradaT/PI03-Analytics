import pandas as pd
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from modules import get_historical_data


# Markets elegidos
coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

coin = st.sidebar.selectbox(
    'Coin', coins)

st.title(f"Predict Future Price - {coin}")

df = get_historical_data(coin)
df = df[['date', 'close']]

df.columns = ["ds", "y"]
m = Prophet()
m.fit(df);

days = st.sidebar.number_input("Days to predict", min_value=1, max_value=365, value=7)

future = m.make_future_dataframe(periods=days)
forecast = m.predict(future)

st.plotly_chart(plot_plotly(m, forecast, ylabel='Price (USD)', xlabel='Days'))