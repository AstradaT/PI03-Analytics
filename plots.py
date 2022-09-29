import matplotlib.pyplot as plt
import pandas as pd
from modules import get_historical_data


coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

crypto = {}

for coin in coins:
    crypto[coin] = get_historical_data(coin)

for coin in crypto:
    print(coin, len(crypto[coin]))

crypto_all = {}

for coin in crypto:
    crypto_all[coin] = crypto[coin]
    crypto[coin] = crypto[coin][-350:]

# Differencing
for coin in crypto:
    crypto[coin]['CloseDiff'] = crypto[coin]['close'].diff().fillna(0)