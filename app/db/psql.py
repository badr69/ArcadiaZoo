import psycopg2
from psycopg2 import pool
import os

psql_pool = None

def init_psql_connection(app):
    global psql_pool
    psql_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        database=os.getenv("PG_DATABASE")
    )

    if psql_pool:
        print("✅ Connexion PostgreSQL établie avec succès.")

def get_psql_connection():
    if psql_pool:
        return psql_pool.getconn()

def release_psql_connection(conn):
    if psql_pool and conn:
        psql_pool.putconn(conn)

def close_psql_pool():
    if psql_pool:
        psql_pool.closeall()
