import functools

import yfinance as yf
import yahooquery as yq
from .user import checkSession
from flask import (Blueprint, redirect, render_template, url_for,request,session)
from ..data import news

bp = Blueprint('news', __name__ , url_prefix='/news')

#getting the news from Yahoo Finance
@bp.route('/', methods = ['GET'])
def getNews():
    user = checkSession()
    #if not user is None:
    #   user = user.get('user_id')
    newsDict = news.getNews()
    return render_template("news.html", news = newsDict, session= user if user else None)
    
