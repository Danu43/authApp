from pymongo import MongoClient
from flask import current_app

mongo_client = None

def init_mongo(app):
    global mongo_client
    mongo_client = MongoClient(app.config["MONGO_URI"])

def get_db():
    if mongo_client is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo(app) first.")
    return mongo_client.get_default_database()
