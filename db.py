# db_connection.py
from pymongo import MongoClient

def get_db_connection():
    # MongoDB URL (local or Atlas connection string)
    client = MongoClient("mongodb://localhost:27017/")  # or use your MongoDB Atlas connection string  # The database
    return client
