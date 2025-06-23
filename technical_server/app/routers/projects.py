from typing import List
from fastapi import APIRouter, Depends
import psycopg

from .. import crud, schemas
from ..database import get_db_connection

router = APIRouter(
    prefix="/projects",
    tags=["projects"], # doc
)

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    sort_by: str = "create_on", 
    order: str = "desc", 
    conn: psycopg.Connection = Depends(get_db_connection)
):
    """
    Récupère la liste de tous les projets. Possiblité de tri
    """
    projects = crud.get_all_projects(conn=conn, sort_by=sort_by, order=order)
    conn.close()
    return projects