// Path: backend/app/api/v1/endpoints/projects.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.db import crud
from app.schemas.project import Project, ProjectCreate
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new saved prompt configuration for the current user.
    """
    return await crud.create_project_with_owner(db=db, project=project_in, owner_id=current_user.id)

@router.get("/", response_model=List[Project])
async def read_projects(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Retrieve all saved prompt configurations for the current user.
    """
    return await crud.get_projects_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)