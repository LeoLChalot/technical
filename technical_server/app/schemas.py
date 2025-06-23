from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schéma pour un projet
class Project(BaseModel):
    id: int
    name: str
    is_active: bool = Field(alias='enabled')
    created_at: datetime = Field(alias='create_on')
    updated_at: datetime = Field(alias='update_on')

    class Config:
        from_attributes = True
        populate_by_name = True

# --- CLASSE MANQUANTE À AJOUTER ---
# Schéma pour un indicateur
class Indicator(BaseModel):
    id: int
    identifier: str
    label: str
    label_short: str
    timeslots: int
    position: int
    asset: Optional[str] = None # 'asset' peut être vide (NULL)

    class Config:
        from_attributes = True