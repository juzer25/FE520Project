from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import current_app, g
from werkzeug.local import LocalProxy

mongo_client = MongoClient("localhost",27017)

def get_db():
    db = mongo_client.stock_db
    return db

db = LocalProxy(get_db)