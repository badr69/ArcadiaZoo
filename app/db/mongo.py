from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "zoo_db")

if not MONGO_URI:
    raise Exception("La variable d'environnement MONGO_URI n'est pas définie !")

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client[MONGO_DB_NAME]

# Définition de la collection reviews
reviews_collection = db["reviews"]


