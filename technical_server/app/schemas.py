from pydantic import BaseModel
from datetime import datetime

class Project(BaseModel):
    id: int
    name: str
    enabled: str
    create_on: datetime
    update_on: datetime

    class Config:
        from_attributes = True