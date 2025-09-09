# import psycopg2
# import traceback
# from app.config import Config
#
# def get_db_connection():
#     """Connexion à la base choisie dans Config.ACTIVE_DB"""
#     try:
#         if Config.ACTIVE_DB == 1:
#             db_name = Config.POSTGRES_DB1
#         else:
#             db_name = Config.POSTGRES_DB2
#
#         conn = psycopg2.connect(
#             host=Config.POSTGRES_HOST,
#             database=db_name,
#             user=Config.POSTGRES_USER,
#             password=Config.POSTGRES_PASSWORD,
#             port=Config.POSTGRES_PORT
#         )
#         return conn
#     except Exception:
#         traceback.print_exc()
#         return None



import psycopg2
from app.config import Config
import traceback

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            port=Config.POSTGRES_PORT
        )
        return conn
    except Exception:
        traceback.print_exc()
        return None




