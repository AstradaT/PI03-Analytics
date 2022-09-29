import streamlit as st
from modules import draw_price_histories, draw_volumes


st.title("Charts")

st.subheader("Compare volumes of transactions")

coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

coins_volumes = st.multiselect("Select coins to plot", coins, default=coins[0:4])

with st.spinner('Drawing chart...'):
    st.pyplot(draw_volumes(coins_volumes))

st.subheader("Compare historical prices")

coins_prices = st.multiselect("Select coins to plot", coins, default=coins[0:2])

with st.spinner('Drawing chart...'):
    st.plotly_chart(draw_price_histories(coins_prices), use_container_width = True)