import psycopg2
import os
import traceback

def get_db_connection():
    try:
        # Récupère l'URL de la BDD depuis la variable d'environnement
        database_url = os.getenv("DATABASE_URL")

        conn = psycopg2.connect(database_url)
        return conn
    except Exception:
        traceback.print_exc()
        return None





# import psycopg2
# from app.config import Config
# import traceback
#
# def get_db_connection():
#     try:
#         conn = psycopg2.connect(
#             host=Config.POSTGRES_HOST,
#             database=Config.POSTGRES_DB,
#             user=Config.POSTGRES_USER,
#             password=Config.POSTGRES_PASSWORD,
#             port=Config.POSTGRES_PORT
#         )
#         return conn
#     except Exception:
#         traceback.print_exc()
#         return None
