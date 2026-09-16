from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://chand37880_db_user:IDS6TzxNqRlJL1yW@scraper.m5aeeba.mongodb.net/?appName=Scraper"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["database"]
collection = db["student_collection"]

def add_userdata(result):
    try:
        collection.insert_one(result)
        print("SUS : Added user info in DB.")
    except Exception:
        print("ERROR : Adding user info in DB.")
    return