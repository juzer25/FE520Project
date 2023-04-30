import os

from flask import Flask, render_template, session

from .routes import stock
from .routes import news
from .routes import user
from .dbconfig import db

app = Flask(__name__ , static_url_path='/' ,instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = 'dev'
        #DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
)


app.register_blueprint(stock.bp)
app.register_blueprint(news.bp)
app.register_blueprint(user.bp)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def index():
    data = user.checkSession()
    if data: 
        return render_template('main.html', session = data['user_id'])
    else:
        return render_template('main.html')
      
