import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # cles secrete de l'application
    SECRET_KEY = os.getenv('SECRET_KEY', 'change me')
    # configuration psql
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    # configuration mongodb
    MONGO_URI = os.getenv('MONGO_URI')


