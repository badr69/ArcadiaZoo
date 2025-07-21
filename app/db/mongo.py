# from pymongo import MongoClient
# from app.config import Config
#
# client = None
# db = None
#
# def init_mongo():
#     global client, db
#     try:
#         client = MongoClient(Config.MONGO_URI)
#         db = client["zoo_db"]
#         print("MongoDB connecté avec succès")
#     except Exception as e:
#         print(f"Erreur connexion MongoDB : {e}")

# import os
# from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient
#
# load_dotenv()
#
# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "zoo_db")
#
# if not MONGO_URI:
#     raise ValueError("❌ MONGO_URI manquant dans .env")
#
# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB_NAME]


from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "zoo_db")

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client[MONGO_DB_NAME]
