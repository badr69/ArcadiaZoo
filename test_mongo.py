from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Charge les variables d'environnement
load_dotenv()

# Récupère l'URI Atlas
uri = os.getenv("MONGO_URI")

if not uri:
    print("❌ Erreur : MONGO_URI non trouvé dans le fichier .env")
    exit()

# Connexion Atlas
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("✅ Connexion réussie à MongoDB Atlas")
except Exception as e:
    print("❌ Erreur de connexion :", e)
