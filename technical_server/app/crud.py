import psycopg
from psycopg.rows import dict_row
from typing import List, Optional, Any
import pandas as pd
from . import schemas

def get_all_projects(conn: psycopg.Connection, sort_by: str = "create_on", order: str = "desc") -> List[schemas.Project]:
    if sort_by not in ["name", "create_on"]:
        sort_by = "create_on"
    if order.lower() not in ["asc", "desc"]:
        order = "desc"

    cursor = conn.cursor(row_factory=dict_row)
    query = f"SELECT id, name, enabled, create_on, update_on FROM projects ORDER BY {sort_by} {order}"
    cursor.execute(query)
    results_as_dicts = cursor.fetchall()
    cursor.close()
    projects = [schemas.Project.model_validate(row) for row in results_as_dicts]
    return projects

def update_project_status(conn: psycopg.Connection, project_id: int, is_active: bool) -> schemas.Project | None:
    cursor = conn.cursor(row_factory=dict_row)
    query = """
        UPDATE projects
        SET enabled = %s, update_on = NOW()
        WHERE id = %s
        RETURNING id, name, enabled, create_on, update_on;
    """
    cursor.execute(query, (is_active, project_id))
    updated_project_dict = cursor.fetchone()
    conn.commit()
    cursor.close()
    if updated_project_dict is None:
        return None
    return schemas.Project.model_validate(updated_project_dict)

# --- FONCTION MANQUANTE À AJOUTER ---
def get_project_by_id(conn: psycopg.Connection, project_id: int) -> schemas.Project | None:
    """Récupère un seul projet par son ID."""
    cursor = conn.cursor(row_factory=dict_row)
    query = "SELECT id, name, enabled, create_on, update_on FROM projects WHERE id = %s"
    cursor.execute(query, (project_id,))
    result_dict = cursor.fetchone()
    cursor.close()
    if result_dict is None:
        return None
    return schemas.Project.model_validate(result_dict)

def get_indicators_for_project(conn: psycopg.Connection, project_id: int) -> List[schemas.Indicator]:
    """Récupère tous les indicateurs associés à un projet spécifique."""
    cursor = conn.cursor(row_factory=dict_row)
    query = """
        SELECT
            i.id, i.identifier, i.label, i.label_short,
            i.timeslots, i.position, i.asset
        FROM indicators i
        JOIN variables v ON i.id = v.indicator
        WHERE v.project = %s
        ORDER BY i.position;
    """
    cursor.execute(query, (project_id,))
    results_as_dicts = cursor.fetchall()
    cursor.close()
    indicators = [schemas.Indicator.model_validate(row) for row in results_as_dicts]
    return indicators

def get_pivoted_numeric_data(
    conn: psycopg.Connection, 
    project_id: int,
    sort_by: Optional[str] = None,
    order: str = "asc"
) -> List[dict[str, Any]]:
    """
    Récupère les données numériques pour un projet, les filtre, les trie et les pivote.
    """
    query = """
        SELECT
            t.begin AS start_time,
            t.end AS end_time,
            i.label_short AS indicator_name,
            n.value
        FROM numerics n
        JOIN variables v ON n.variable = v.id
        JOIN indicators i ON v.indicator = i.id
        JOIN times t ON n.time = t.id
        WHERE v.project = %s;
    """
    df = pd.read_sql(query, conn, params=(project_id,))

    if df.empty:
        return []

    pivot_df = df.pivot_table(
        index=['start_time', 'end_time'], 
        columns='indicator_name', 
        values='value',
        aggfunc='sum'
    ).reset_index()

    if sort_by and sort_by in pivot_df.columns:
        ascending = order.lower() == 'asc'
        pivot_df = pivot_df.sort_values(by=sort_by, ascending=ascending)

    pivot_df = pivot_df.rename(columns={'start_time': 'Temps de début', 'end_time': 'Temps de fin'})

    return pivot_df.to_dict(orient='records')