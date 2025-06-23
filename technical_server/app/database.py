import psycopg
from .settings import settings

# Création d'un pool de connexion
conn_pool = psycopg.conninfo.conninfo_to_dict(settings.database_url)

def get_db_connection():
    # Nouvelle connexion à partir du pool.
    # Injection des connexion aux routes
    conn = psycopg.connect(**conn_pool)
    return conn