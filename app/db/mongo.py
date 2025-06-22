from pymongo import MongoClient
from app.config import Config

def get_mongo_client():
    try:
        client = MongoClient(Config.MONGO_URI)
        return client
    except Exception as e:
        print(f"Erreur connexion MongoDB : {e}")
        return None
