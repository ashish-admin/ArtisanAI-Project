# app/db/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import base as models
from app.schemas import project as project_schema
from app.schemas import user as user_schema

# --- User CRUD Functions ---

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Retrieves a single user from the database by their ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Retrieves a single user from the database by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate, hashed_password: str) -> models.User:
    """
    Creates a new user record in the database.
    Note: This function accepts an already hashed password.
    """
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- Project CRUD Functions ---

def get_projects_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Project]:
    """
    Retrieves a list of projects for a specific user.
    """
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).offset(skip).limit(limit).all()


def create_user_project(db: Session, project: project_schema.ProjectCreate, owner_id: int) -> models.Project:
    """
    Creates a new writing project record for a specific user.
    """
    db_project = models.Project(
        **project.model_dump(),  # Unpacks the Pydantic model into keyword arguments
        owner_id=owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int, owner_id: int) -> Optional[models.Project]:
    """
    Retrieves a single project by its ID, ensuring it belongs to the specified owner.
    """
    return db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == owner_id).first()


def update_project(db: Session, project_id: int, project_update: project_schema.ProjectUpdate, owner_id: int) -> Optional[models.Project]:
    """
    Updates an existing project, ensuring it belongs to the specified owner.
    """
    db_project = get_project(db, project_id, owner_id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int, owner_id: int) -> Optional[models.Project]:
    """
    Deletes a project by its ID, ensuring it belongs to the specified owner.
    """
    db_project = get_project(db, project_id, owner_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project