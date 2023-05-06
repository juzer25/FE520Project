﻿import os
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
from bs4 import BeautifulSoup
import requests as req
bp = Blueprint('stock' , __name__ , url_prefix='/stock')

#Specific company search
@bp.route('/get', methods = ['GET'])
def getStockInfo():
    try:
        search = request.args.get("search")
        #print("here ",search)
        if search is None:
            return redirect(url_for('index'))
        if search.isspace():
            return redirect(url_for('index'))
        session = checkSession()
        #D(ib) Va(m) Maw(65%) Ov(h)
        summary = stock.stockSummary(search)
        #print(summary)
        #plot = stock.getGraph(search)
        #print(plot)
        quote = stock.quoteScraping(search)
        #print(quote)
        if session: 
            userData = uData.userInfo(session.get('user_id'))
        #print(postMarket.Time)
            if not userData is None:
                if search not in userData['tickers']:
                    userData['tickers'].append(search)
                    res = uData.updateTicker(userData)
    except Exception as e:
        return render_template('error.html', error=e)
    except BaseException as base:
        return render_template('error.html', error=base)
    except IOError as err:
        return {"error" : str(err)}
    return render_template("stock.html",sym = search,
                           summary = summary, quote=quote,session=session if session else None )

#Company tracking
@bp.route('/<name>', methods = ['GET'])
def getTrackingStock(name):
    try:
        #search = request.args.get("search")
        userData = checkSession()
        #D(ib) Va(m) Maw(65%) Ov(h)
        summary = stock.stockSummary(name)
        #plot = stock.getGraph(search)
        #print(plot)
        quote = stock.quoteScraping(name)
       
                
    except IOError as err:
        return {"error" : str(err)}
    return render_template("stock.html",sym = name,
                           summary = summary, quote=quote, session=session if session else None )


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
                            plot=plot_json, session=session if session else None)

   
   
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
    try:
        userSession = checkSession()

        if userSession:
            userSession = userSession.get('user_id')
    
        symbols = request.args.get('symbols')
    #When there is no compare strings
        if symbols is None:
            return render_template('compare.html', session = session if session else None)
        print(symbols)
        if ',' in symbols:
            symbols =symbols.split(',')
            symbols = ' '.join(symbols)
        data = stock.compare(symbols)
    except Exception as e:
        return render_template('error.html', error=e)
    return render_template('compare.html', plot = data, session = session if session else None)

@bp.route('/company', methods=['GET'])
def getCompanyProfile():
    try:
        search = request.args.get('search')
        print(search)
        if search is None:
            return render_template('error.html')
        data = stock.getCompanyProfile(search)
        return render_template('company.html', data=data, sym=search, session=session if session else None)
    except BaseException as e:
        print(e)
        return render_template('error.html ')