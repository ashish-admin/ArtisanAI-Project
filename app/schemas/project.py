app/schemas/project.py
from pydantic import BaseModel
from typing import Optional

--- Shared Base Schema ---
Defines the common attributes of a writing project.
class ProjectBase(BaseModel):
"""
Base Pydantic model for a Project.
"""
name: str
writing_text: str
critique_goal: str
critique_persona: Optional[str] = None

--- Schemas for Specific Use Cases ---
class ProjectCreate(ProjectBase):
"""
Schema for creating a new project. It has the same fields as the base.
This is used as the request body for the project creation endpoint.
"""
pass

class ProjectUpdate(BaseModel):
"""
Schema for updating an existing project. All fields are optional
to allow for partial updates.
"""
name: Optional[str] = None
writing_text: Optional[str] = None
critique_goal: Optional[str] = None
critique_persona: Optional[str] = None
critique_result_text: Optional[str] = None # The critique result can also be updated

class Project(ProjectBase):
"""
Schema for returning a project in an API response.
It includes all base fields plus the database ID, owner ID,
and the critique result.
"""
id: int
owner_id: int
critique_result_text: Optional[str] = None

class Config:
    """
    Pydantic V2 configuration to enable ORM mode (from_attributes).
    This allows the Pydantic model to be created directly from the
    SQLAlchemy Project model instance.
    """
    from_attributes = True
