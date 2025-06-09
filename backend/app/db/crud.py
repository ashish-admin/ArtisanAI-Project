# Path: backend/app/db/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.base import User, Project
from app.schemas.user import UserCreate
from app.schemas.project import ProjectCreate
from app.services.security import get_password_hash

# --- User CRUD ---

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Project CRUD ---

async def get_projects_by_owner(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
    result = await db.execute(
        select(Project)
        .filter(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .order_by(Project.updated_at.desc())
    )
    return result.scalars().all()

async def create_project_with_owner(db: AsyncSession, project: ProjectCreate, owner_id: int) -> Project:
    db_project = Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project