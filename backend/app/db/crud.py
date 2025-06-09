# backend/app/db/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.base import User, Project
from app.schemas.user import UserCreate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.security import get_password_hash
from typing import List, Optional

# --- User CRUD ---

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Retrieve a user from the database by their email address.
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Project CRUD ---

async def get_project(db: AsyncSession, project_id: int, owner_id: int) -> Optional[Project]:
    """
    Retrieve a single project by its ID, ensuring it belongs to the owner.
    """
    result = await db.execute(
        select(Project).filter(Project.id == project_id, Project.owner_id == owner_id)
    )
    return result.scalars().first()

async def get_projects_by_owner(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
    """
    Retrieve all projects for a specific owner with pagination.
    """
    result = await db.execute(
        select(Project)
        .filter(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .order_by(Project.updated_at.desc())
    )
    return result.scalars().all()

async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int) -> Project:
    """
    Create a new project for a user.
    """
    db_project = Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

async def update_project(db: AsyncSession, db_project: Project, project_in: ProjectUpdate) -> Project:
    """
    Update an existing project.
    """
    project_data = project_in.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    await db.commit()
    await db.refresh(db_project)
    return db_project

async def delete_project(db: AsyncSession, project_id: int, owner_id: int) -> Optional[Project]:
    """
    Delete a project by its ID, ensuring it belongs to the owner.
    """
    db_project = await get_project(db, project_id=project_id, owner_id=owner_id)
    if db_project:
        await db.delete(db_project)
        await db.commit()
    return db_project