import streamlit as st
import pandas as pd
import requests
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

pio.renderers.default='browser'

# Source: https://gist.github.com/GrovesD2/d2dbf1def86fddf4dcf6d9dcb0a8fec6#file-complex_candlestick-py
def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    ticker : str
        The ticker we are plotting (for the title).
    '''
    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = (f'{ticker} Stock Price', 'Volume Chart'),
        row_width = [0.3, 0.7]
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['date'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Scatter(x=df['date'], y=df[f'{ma1}_ma'], mode='lines', name=f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Scatter(x = df['date'], y = df[f'{ma2}_ma'], mode='lines', name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Bar(x = df['date'], y = df['volume'], name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    
    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    return fig

# Get historical prices
@st.cache(allow_output_mutation=True)
def get_historical_data(coin):
    resolution = 60 * 60 * 24
    url = f'https://ftx.com/api/markets/{coin}/USD/candles?resolution={resolution}'
    request = requests.get(url).json()
    df = pd.DataFrame(request['result'])
    df['date'] = pd.to_datetime(df['startTime']).dt.date
    df = df.drop(columns=['startTime', 'time'])
    return df