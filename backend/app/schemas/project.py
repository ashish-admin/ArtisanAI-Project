# backend/app/schemas/project.py

from pydantic import BaseModel
import datetime

# Base properties for a project
class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    original_text: str

# Properties to receive on project creation
class ProjectCreate(ProjectBase):
    pass

# Properties to receive on project update
class ProjectUpdate(ProjectBase):
    pass

# Properties stored in the database
class ProjectInDB(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    critique_text: str | None = None

    class Config:
        from_attributes = True # Changed from orm_mode

# Properties to return to the client
class Project(ProjectInDB):
    pass