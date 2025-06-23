from pymongo import MongoClient
from app.config import Config

try:
    client = MongoClient(Config.MONGO_URI)
    # Test simple : liste des bases de données
    dbs = client.list_database_names()
    print("Connexion MongoDB réussie ! Bases disponibles :", dbs)
    client.close()
except Exception as e:
    print("Erreur connexion MongoDB :", e)










# from pymongo import MongoClient
# from app.config import MONGO_URI
#
# try:
#     client = MongoClient(MONGO_URI)
#     # Test simple : liste des bases de données
#     dbs = client.list_database_names()
#     print("Connexion MongoDB réussie ! Bases disponibles :", dbs)
#     client.close()
# except Exception as e:
#     print("Erreur connexion MongoDB :", e)
