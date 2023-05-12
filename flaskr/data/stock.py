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
from pandas import Timestamp
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
import plotly.express as px
import plotly
import json
import datetime as datetime
import numpy as np
from ..dbconfig import db
from deepdiff import DeepDiff

#Helper functions------------------------------------------------
#Creating graphs for comparing Ticker
def createCompareGraph(df, symbols):
    trace = px.line(df, x="date",y="adjclose", color='symbol')
    trace.update_layout(title = "Compareing closing_price with date between tickers "+symbols)
    plot_json = json.dumps(trace, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

#Preparing data to provide it for ploting graph
def prepareDf(search,df):
    #converting data to json
    temp = db.stock.find_one({"symbol":search.lower()})

    df = df.to_json(orient="table")
    #print(df)
    df= json.loads(df)

    if temp is None:
        store = {
            "symbol":search.lower(),
            "data": df['data']
        }
        insertedStock = db.stock.insert_one(store)
        if insertedStock.inserted_id is None:
            raise Exception("Something went wrong")
    else:
        #Library that will find difference in json and return the difference
        deepdiff = DeepDiff(df['data'], temp['data'])
        if deepdiff:
            db.stock.update_one(
                {"_id": temp['_id']},
                {"$set":{"data":df['data']}}
            )
        else:
            
            df['data'] = temp['data']

    table = df['data']
    #print(table)
    #making a dictionary for each row
    fields  = df['schema']['fields']
    dict = {}
    j=0
    for i in df['data']:
        dict[j] = i
        j += 1
    #converting to Dataframe
    df = pd.read_json(json.dumps(dict), orient="index")
    #cleaning Date column and then returning
    if isinstance(df['date'][0], str):
        #print(df['date'].str.contains('Z').value_counts())
        df['date'].mask(df['date'].str.contains('Z'), df['date'].str.replace('Z', ''), inplace=True)
        #print(df['date'].str.contains('Z').value_counts())
        #print(df['date'])
        df['date'] = pd.to_datetime(df['date'])
        return {"data" : df, "fields":fields, "table":table}
    else:
        pd.DatetimeIndex(df['date'])
        df['date'] = pd.to_datetime(df['date'], format)
        #print(df.head(13))
        #print("here")
        return {"data" : df, "fields":fields, "table":table}
#-------------------------------------------------

#getting stock history data
def getHistory(search, period='1y', interval='1h'):
    #print("period - ",period)
    #print("interval - ",interval)
    data = yq.Ticker(search, asynchronous=True)
    historyInfo = data.history(period=period, interval=interval)
    if historyInfo.empty:
        raise Exception("Data is empty or no Ticker for %s"%search)
    #preparing the data for rendering and creating graph
    historyInfo = prepareDf(search,historyInfo)
    
    return historyInfo

#getting company summary
def stockSummary(search):
    data = yq.Ticker(search)
    summary = data.summary_detail
    #print(summary)
    #checking if the ticker exists
    if summary[search] == 'Quote not found for ticker symbol: '+search.upper():
        raise Exception(summary[search])
    return summary[search]

#To compare multiple tickers
#Reference - https://yahooquery.dpguthrie.com/guide/ticker/intro/
def compare(symbols):
    symCheck = symbols
    symCheck = symCheck.split(" ")
    #check if the ticker symbol exists
    for i in symCheck:
        #print(i)
        temp = yq.Ticker(i)
        temp = temp.summary_detail
        #print(temp)
        if temp[i] == 'Quote not found for ticker symbol: '+i.upper():
            #print("here")
            raise Exception(temp[i])
    data = Ticker(symbols)
    #print(data)
    data = data.history()
    
    df = data.reset_index()
    df = pd.DataFrame(df)
    #print(df)
    #print(type(df['date']))
    #df = prepareDf(df)
    #print(df)
    return createCompareGraph(df,symbols)


#Not using, but made this for reference
# Reference - https://www.tutorialspoint.com/how-to-show-matplotlib-in-flask   
#need to reuse this
#Generate graph for history
'''def getGraph(search):
     # Set the URL for the stock you want to get data for
    # Extract the graph data from the JSON
    dates = data['chart']['result'][0]['timestamp']
    closing_prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
    # Create a Plotly figure with the closing prices over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=closing_prices, mode='lines'))
    # Customize the layout of the figure
    #print("made plot")
    fig.update_layout(title='TSLA Closing Prices', xaxis_title='Date', yaxis_title='Closing Price')
    # Convert the figure to JSON and pass it to the Jinja template
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #print(type(plot_json))
    return plot_json
'''
#getting top trending quotes
def getTrendingStock():
    trending = yq.get_trending()
    data = []
    for quote in trending['quotes']:
        data.append(quote['symbol'])
    #print(data)
    res = yq.Ticker(data)
    return data


#get company information
def getCompanyProfile(symbol):
    temp = yq.Ticker(symbol)
    temp = temp.summary_detail
        #print(temp)
    if temp[symbol] == 'Quote not found for ticker symbol: '+symbol.upper():
            #print("here")
        raise Exception(temp[symbol])
    data = yq.Ticker(symbol)
    if not data is None:
        data = data.summary_profile
        return data[symbol]
    else:
        raise Exception("Ticker not found!!")

#getting the quotes from Yahoo Finance website   
def quoteScraping(search):
    #Request the webpage
    res = requests.get('https://finance.yahoo.com/quote/'+search.upper())
    #usin BeautifulSoup to parse the html
    soup = BeautifulSoup(res.text, "html.parser")
    htmlData = soup.findAll('div', class_="D(ib) Va(m) Maw(65%) Ov(h)")
    #print(htmlData)
    #getting the data by finding specific HTML elements
    regularMarketPrice = soup.find(
        'fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")
    #print(regularMarketPrice)
    regularMarketChange = soup.find(
        'fin-streamer', class_="Fw(500) Pstart(8px) Fz(24px)")
    #print(regularMarketPrice.text)
    #print(regularMarketChange.findChild().text)
    #regularMarketChangePerc = soup.find('fin-streamer', class_="Fw(500) Pstart(8px) Fz(24px)")
    regularMarketChangePerc = regularMarketChange.find_next_sibling().findChild().text
    #print(regularMarketChangePerc)
    regularMarketChange = regularMarketChange.text
    regularMarketPrice = regularMarketPrice.text
    atClose = soup.find('div', id="quote-market-notice")
    atClose = atClose.findChild().text
    #print(atClose)
    #############################
    postMarketPrice = soup.find(
        'fin-streamer', class_="C($primaryColor) Fz(24px) Fw(b)")
    #print(postMarketPrice)
    #print("postmarket")
    if not postMarketPrice is None: 
        postMarketPrice = postMarketPrice.text
        #print(postMarketPrice)
        postMarketChange = soup.find(
        'fin-streamer', class_="Mstart(4px) D(ib) Fz(24px)")

        #print(postMarketChange.text)
        postMarketChangePerc = postMarketChange.find_next_sibling().findChild().text
        #print(postMarketChangePerc)
        postMarketChange = postMarketChange.text
        timePart = soup.find(
        'span', class_="C($tertiaryColor) Fz(12px) smartphone_Fz(xs)")
        afterClose = timePart.findChild()
        #print(afterClose)
        postMarketTime = afterClose.findNextSibling().text
        afterClose = afterClose.text
    else:
        postMarketPrice = None
        postMarketChange = None
        postMarketChangePerc=None
        afterClose=None
        postMarketTime = None
        
    quote = {
        "regularMarketPrice": regularMarketPrice,
        "regularMarketChange": regularMarketChange,
        "regularMarketChangePerc": regularMarketChangePerc,
        "atClose": atClose,
        "postMarketPrice": postMarketPrice,
        "postMarketChange": postMarketChange,
        "postMarketChangePerc": postMarketChangePerc,
        "afterClose": afterClose,
        "postMarketTime": postMarketTime
    }
    #print(quote)
    return quote

#getting specific company news
def getCompanyNews(search):
    if search is None:
        raise Exception("something went wrong")
    #validating if ticker exist
    temp = yq.Ticker(search)
    temp = temp.summary_detail
        #print(temp)
    if temp[search] == 'Quote not found for ticker symbol: '+search.upper():
            #print("here")
        raise Exception(temp[search])
    data = yf.Ticker(search)
    data = data.news
    return data
