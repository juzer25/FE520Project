import os

from flask import Flask, render_template, session
from flask_cors import CORS
from .routes import stock
from .routes import news
from .routes import user
from .dbconfig import db
from .routes import posts
from .data.stock import getTrendingStock
app = Flask(__name__ , static_url_path='/' ,instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = 'dev'
        #DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
)

#Cross-origin resource sharing (CORS) is a browser security feature that restricts HTTP requests that are initiated from scripts running in the browser.
cors = CORS(app)
#Registering routes
#reference - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/
app.register_blueprint(stock.bp)
app.register_blueprint(news.bp)
app.register_blueprint(user.bp)
app.register_blueprint(posts.bp)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def index():
    data = user.checkSession()
    trending = getTrendingStock()
    #print(trending)
    return render_template('main.html', trending=trending,session = session if session else None)
      
@app.route('/about')
def about():
    return render_template('about.html',session = session if session else None)