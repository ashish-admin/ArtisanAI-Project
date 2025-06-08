app/api/v1/endpoints/projects.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.db import crud
from app.schemas import project as project_schema
from app.db.base import User # Used for type hinting the current_user dependency

Create a new API router for project-related endpoints
router = APIRouter()

@router.post("/", response_model=project_schema.Project, status_code=status.HTTP_201_CREATED)
def create_project(
*,
db: Session = Depends(deps.get_db),
project_in: project_schema.ProjectCreate,
current_user: User = Depends(deps.get_current_active_user),
) -> Any:
"""
Create a new writing project for the current user.
"""
project = crud.create_user_project(db=db, project=project_in, owner_id=current_user.id)
return project

@router.get("/", response_model=List[project_schema.Project])
def read_projects(
db: Session = Depends(deps.get_db),
skip: int = 0,
limit: int = 100,
current_user: User = Depends(deps.get_current_active_user),
) -> Any:
"""
Retrieve a list of projects for the current user.
Supports pagination with skip and limit parameters.
"""
projects = crud.get_projects_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
return projects

@router.get("/{project_id}", response_model=project_schema.Project)
def read_project(
*,
db: Session = Depends(deps.get_db),
project_id: int,
current_user: User = Depends(deps.get_current_active_user),
) -> Any:
"""
Get a specific project by ID.
Ensures the project belongs to the current user.
"""
project = crud.get_project(db, project_id=project_id, owner_id=current_user.id)
if not project:
raise HTTPException(status_code=404, detail="Project not found")
return project

@router.put("/{project_id}", response_model=project_schema.Project)
def update_project(
*,
db: Session = Depends(deps.get_db),
project_id: int,
project_in: project_schema.ProjectUpdate,
current_user: User = Depends(deps.get_current_active_user),
) -> Any:
"""
Update a user's writing project.
"""
project = crud.get_project(db, project_id=project_id, owner_id=current_user.id)
if not project:
raise HTTPException(
status_code=404,
detail="Project not found",
)
project = crud.update_project(db=db, project_id=project_id, project_update=project_in, owner_id=current_user.id)
return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
*,
db: Session = Depends(deps.get_db),
project_id: int,
current_user: User = Depends(deps.get_current_active_user),
) -> None:
"""
Delete a user's writing project.
"""
project = crud.get_project(db, project_id=project_id, owner_id=current_user.id)
if not project:
raise HTTPException(
status_code=404,
detail="Project not found",
)
crud.delete_project(db=db, project_id=project_id, owner_id=current_user.id)
return None