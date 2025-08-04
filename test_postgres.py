import psycopg2
from dotenv import load_dotenv
from app.config import Config

load_dotenv()

try:
    print("✅ Connexion réussie à PostgreSQL")
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
