from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "zoo_db")

try:
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    db = client[MONGO_DB_NAME]
    reviews_collection = db["reviews"]
except Exception:
    traceback.print_exc()
    client = None
    db = None
    reviews_collection = None



# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "zoo_db")
#
# client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
# db = client[MONGO_DB_NAME]
#
# # Définition de la collection reviews
# reviews_collection = db["reviews"]
