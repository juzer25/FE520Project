import functools

import yfinance as yf
import yahooquery as yq

from flask import (Blueprint, redirect, render_template, url_for,request)
from ..data import news

bp = Blueprint('news', __name__ , url_prefix='/news')

@bp.route('/', methods = ['GET'])
def getNews():
    newsDict = news.getNews()
    return render_template("news.html", news = newsDict)
    
