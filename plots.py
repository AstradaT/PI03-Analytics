import matplotlib.pyplot as plt
from modules import get_historical_data


coins = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL',
    'DOGE', 'MATIC', 'TRX', 'LTC', 'UNI']

crypto = {}

for coin in coins:
    crypto[coin] = get_historical_data(coin)

for coin in crypto:
    print(coin, len(crypto[coin]))