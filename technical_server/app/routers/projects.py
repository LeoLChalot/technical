from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
import psycopg
from pydantic import BaseModel

from .. import crud, schemas
from ..database import get_db_connection

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    sort_by: str = "create_on",
    order: str = "desc",
    conn: psycopg.Connection = Depends(get_db_connection)
):
    projects = crud.get_all_projects(conn=conn, sort_by=sort_by, order=order)
    conn.close()
    return projects

class ProjectStatusUpdate(BaseModel):
    is_active: bool

@router.patch("/{project_id}", response_model=schemas.Project)
def update_project_status(
    project_id: int,
    status_update: ProjectStatusUpdate,
    conn: psycopg.Connection = Depends(get_db_connection)
):
    updated_project = crud.update_project_status(
        conn=conn,
        project_id=project_id,
        is_active=status_update.is_active
    )
    if updated_project is None:
        # Syntaxe modifiée
        raise HTTPException(404, detail="Project not found")
    conn.close()
    return updated_project

@router.get("/{project_id}/indicators", response_model=List[schemas.Indicator])
def read_project_indicators(
    project_id: int,
    conn: psycopg.Connection = Depends(get_db_connection)
):
    project = crud.get_project_by_id(conn=conn, project_id=project_id)
    if project is None:
        # Syntaxe modifiée
        raise HTTPException(404, detail="Project not found")
    indicators = crud.get_indicators_for_project(conn=conn, project_id=project_id)
    conn.close()
    return indicators

@router.get("/{project_id}/data", response_model=List[dict[str, Any]])
def read_project_numeric_data(
    project_id: int,
    sort_by: Optional[str] = None,
    order: str = "asc",
    conn: psycopg.Connection = Depends(get_db_connection)
):
    project = crud.get_project_by_id(conn=conn, project_id=project_id)
    if project is None:
        conn.close()
        # Syntaxe modifiée
        raise HTTPException(404, detail="Project not found")
    if not project.is_active:
        conn.close()
        # Syntaxe modifiée
        raise HTTPException(403, detail="Project is not active")
    
    data = crud.get_pivoted_numeric_data(
        conn=conn,
        project_id=project_id,
        sort_by=sort_by,
        order=order
    )
    conn.close()
    return data