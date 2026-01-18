from pymongo import MongoClient

client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")
db = client["medical_ai"]
reports_collection = db["reports"]
