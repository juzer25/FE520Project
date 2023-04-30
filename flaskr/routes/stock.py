import os
import functools
import json
import yfinance as yf
import yahooquery as yq
from ..data import user as uData
from ..data import stock
from .user import checkSession
from flask import (Blueprint, redirect, render_template, url_for,request,session, jsonify)
from flask_plots import Plots
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import mplfinance as mpf
import plotly.graph_objects as go
import plotly
bp = Blueprint('stock' , __name__ , url_prefix='/stock')

#Specific company search
@bp.route('/get', methods = ['GET'])
def getStockInfo():
    try:
        search = request.args.get("search")
        userData = checkSession()
        
        summary = stock.stockSummary(search)
        #plot = stock.getGraph(search)
        #print(plot)
        if not userData is None:
            if search not in userData['tickers']:
                userData['tickers'].append(search)
                res = uData.updateTicker(userData)
                
    except IOError as err:
        return {"error" : str(err)}
    return render_template("stock.html",sym = search,
                           summary = summary)

#Getting company history
@bp.route("/history", methods=['GET'])
def getHistory():
    try:
        print(request.args)
        search = request.args.get("search")
        period = request.args.get("period")
        interval = request.args.get("interval")
        if not(period is None or interval is None):
            if period == '' and interval == '':
                data = stock.getHistory(search=search)
            elif period == '' and interval != '':
                data = stock.getHistory(search=search, interval=interval)
            elif period != '' and interval == '':
                data = stock.getHistory(search=search, period=period)
            else:
                data = stock.getHistory(search=search, period=period, interval=interval)
        else:
            data = stock.getHistory(search=search)
        #data = json.loads(data)
        print(data)

        fields  = data['fields']
       
        '''dict = {}
        j=0
        for i in data['data']:
            dict[j] = i
            j += 1'''
        df = data['data']
        table = data['table']
        
        #df = pd.read_json(json.dumps(dict), orient="index")
        #df.index = pd.DatetimeIndex(df['date'])
        trace = go.Candlestick(
            x=df.index.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
            open=df["open"].tolist(),
            high=df["high"].tolist(),
            low=df["low"].tolist(),
            close=df["close"].tolist(),
            name=search,
        )

        fig = go.Figure()
        fig.add_trace(trace)
        fig.update_layout(title = "Historiacal data")
        

        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        #plot = mpf.plot(df, type="candle")
    except IOError as err:
        return {"error" : str(err)}
    return render_template("history.html", fields = fields, data = table ,sym = search,
                            plot=plot_json)

   
@bp.route('/getSummary', methods = ['GET'])
def getStockSummary():
    pass

@bp.route('/trending', methods = ['GET'])
def getTrendingStock():
    #print(res.financial_data)
    res = stock.getTrendingStock()
    return res
    

@bp.route('/market', methods = ['GET'])
def getMarketSummary():
    return stock.getMarketSummary()

@bp.route('/compare', methods=['GET'])
def getComparison():
    symbols = request.args.get('symbols')
    if symbols is None:
        return render_template('compare.html')
    print(symbols)
    if ',' in symbols:
        symbols =symbols.split(',')
        symbols = ' '.join(symbols)
    
    data = stock.compare(symbols)
    return render_template('compare.html', plot = data)

@bp.route('/company', methods=['GET'])
def getCompanyProfile():
    try:
        search = request.args.get('search')
        print(search)
        if search is None:
            return render_template('error.html')
        data = stock.getCompanyProfile(search)
        return render_template('company.html', data=data, sym=search)
    except BaseException as e:
        print(e)
        return render_template('error.html ')