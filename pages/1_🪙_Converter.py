import streamlit as st
import requests


def convert_currency(from_coin, to_coin, amount):
    if from_coin == to_coin:
        if from_coin == 'USD' and to_coin == 'USD':
            return amount
        else:
            request = requests.get(f'https://ftx.com/api/markets/{from_coin}/USD').json()
            price = request['result']['price']
            return amount * price
    else:
        if from_coin == 'USD':
            from_price = 1
            request = requests.get(f'https://ftx.com/api/markets/{to_coin}/USD').json()
            to_price = request['result']['price']
            return (from_price / to_price) * amount
        elif to_coin == 'USD':
            request = requests.get(f'https://ftx.com/api/markets/{from_coin}/USD').json()
            from_price = request['result']['price']
            return from_price * amount
        else:
            request = requests.get(f'https://ftx.com/api/markets/{from_coin}/USD').json()
            from_price = request['result']['price']
            request = requests.get(f'https://ftx.com/api/markets/{to_coin}/USD').json()
            to_price = request['result']['price']
            rate = from_price / to_price
            return amount * rate


st.title("Currency Converter")

coins = ['USD', 'BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

col1, col2 = st.columns(2)

coin1 = col1.selectbox(
    'Convert', coins, index=1)

coin2 = col1.selectbox(
    'To', coins, index=0)

amount = col2.number_input("Amount", min_value=0.0, value=1.0)
col2.metric("Converted", convert_currency(coin1, coin2, amount))

