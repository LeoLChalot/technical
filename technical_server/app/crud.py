import psycopg
from psycopg.rows import class_row
from . import schemas

def get_all_projects(conn: psycopg.Connection, sort_by: str = "create_on", order: str = "desc"):
    # Eviter les injections
    if sort_by not in ["name", "create_on"]:
        sort_by = "create_on"
    if order.lower() not in ["asc", "desc"]:
        order = "desc"

    # Exec de la request
    cursor = conn.cursor(row_factory=class_row(schemas.Project))
    
    # Requête préparée
    query = f"SELECT id, name, enabled, create_on, update_on FROM projects ORDER BY {sort_by} {order}"
    
    cursor.execute(query)
    
    projects = cursor.fetchall()
    cursor.close()
    
    return projects