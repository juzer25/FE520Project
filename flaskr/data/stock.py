import yfinance as yf
import yahooquery as yq
from yahooquery import Ticker
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import mplfinance as mpf
from flask import Response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
import plotly.express as px
import plotly
import json

#Helper functions------------------------------------------------
def createCompareGraph(df):
    trace = px.line(df, x="date",y="adjclose", color='symbol')
    
    trace.update_layout(title = "Compareing closing_price with date between tickers")
    plot_json = json.dumps(trace, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def prepareDf(df):
    df = df.to_json(orient="table")
    df= json.loads(df)
    table = df['data']
    #print(df['data'])
    fields  = df['schema']['fields']
    dict = {}
    j=0
    for i in df['data']:
        dict[j] = i
        j += 1
    # = json.loads(df)
    df = pd.read_json(json.dumps(dict), orient="index")
    df.index = pd.DatetimeIndex(df['date'])
    return {"data" : df, "fields":fields, "table":table}
#-------------------------------------------------


def getHistory(search, period='1y', interval='1h'):
    print("period - ",period)
    print("interval - ",interval)
    data = yq.Ticker(search)
    historyInfo = data.history(period=period, interval=interval)
    if historyInfo.empty:
        raise IOError("Data is empty or no Ticker for %s"%search)
    
    historyInfo = prepareDf(historyInfo)

    return historyInfo

def stockSummary(search):
    data = yq.Ticker(search)
    summary = data.summary_detail
    #print(type(summary))
    return summary[search]


def compare(symbols):
    data = Ticker(symbols)
    data = data.history()
    #print(data)
    df = data.reset_index()
    df = pd.DataFrame(df)
    #print(type(df['date']))
    df = prepareDf(df)
    #print(df)
    return createCompareGraph(df['data'])


    
#need to reuse this
#Generate graph for history
def getGraph(search):
     # Set the URL for the stock you want to get data for
    # Extract the graph data from the JSON
    dates = data['chart']['result'][0]['timestamp']
    closing_prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
    # Create a Plotly figure with the closing prices over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=closing_prices, mode='lines'))
    # Customize the layout of the figure
    print("made plot")
    fig.update_layout(title='TSLA Closing Prices', xaxis_title='Date', yaxis_title='Closing Price')
    # Convert the figure to JSON and pass it to the Jinja template
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(type(plot_json))
    return plot_json

def getTrendingStock():
    trending = yq.get_trending()
    data = []
    for quote in trending['quotes']:
        data.append(quote['symbol'])
    res = yq.Ticker(data)
    return res.price

def getMarketSummary():
    return yq.get_market_summary()

def getCompanyProfile(symbol):
    data = yq.Ticker(symbol)
   
    if not data is None:
 
        data = data.summary_profile
        return data[symbol]
    else:
        raise BaseException("Ticker not found!!")
    
