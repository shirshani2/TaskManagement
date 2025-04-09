import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

# טוען את משתני הסביבה מהקובץ .env
load_dotenv()

# משתמש במשתנה הסביבה
cluster = MongoClient(os.getenv("MONGO_URI"))
db = cluster["taskManager"]
users_collection = db["users"]
tasks_collection = db["tasks"]
ai_collection = db["ai_recommendations"]
