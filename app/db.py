import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://shirshani17:1234@cluster0.pvsjjnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["taskManager"]
users_collection = db["users"]

# post = {"_id": 0, "name": "tim"}
# collection.insert_one(post)
# אפשר גם לעשות list ולהכניס many