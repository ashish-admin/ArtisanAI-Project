# backend/app/api/v1/endpoints/projects.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.db import crud
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new writing project.
    """
    return await crud.create_project(db=db, project=project_in, owner_id=current_user.id)

@router.get("/", response_model=List[Project])
async def read_projects(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Retrieve all projects for the current user.
    """
    return await crud.get_projects_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=Project)
async def read_project(
    project_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a specific project by ID.
    """
    db_project = await crud.get_project(db, project_id=project_id, owner_id=current_user.id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a project.
    """
    db_project = await crud.get_project(db, project_id=project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return await crud.update_project(db=db, db_project=db_project, project_in=project_in)

@router.delete("/{project_id}", response_model=Project)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a project.
    """
    deleted_project = await crud.delete_project(db=db, project_id=project_id, owner_id=current_user.id)
    if not deleted_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return deleted_project