import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'mydb')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')

# Configuration MongoDB en dehors de la classe (directement accessible)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["zoo_db"]