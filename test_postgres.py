from dotenv import load_dotenv
load_dotenv()  # Charge les variables .env

import psycopg2
from app.config import Config

try:
    conn = psycopg2.connect(
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        dbname=Config.POSTGRES_DB
    )
    print("Connexion PostgreSQL réussie !")
    conn.close()
except Exception as e:
    print("Erreur connexion PostgreSQL :", e)
