import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://shirshani17:1234@cluster0.pvsjjnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["taskManager"]
users_collection = db["users"]
tasks_collection = db["tasks"]


