# artisan_ai_backend/app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from typing import List, Optional

from app import models

# --- User CRUD ---
def get_user_by_email(db: Session, email: str) -> Optional[models.UserDB]:
    """Retrieves a single user from the database by their email address."""
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def create_user(db: Session, user: models.UserCreate, hashed_password: str) -> models.UserDB:
    """Creates a new user record in the database with an already hashed password."""
    db_user = models.UserDB(email=user.email, hashed_password=hashed_password, is_active=True)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise
    return db_user

# --- Prompt Configuration CRUD ---
def create_prompt_configuration(db: Session, config: models.PromptConfigurationCreate, owner_id: int) -> models.PromptConfigurationDB:
    """Creates a new prompt configuration record for a specific user."""
    constraints_json_str = config.constraints.model_dump_json()
    db_config = models.PromptConfigurationDB(
        name=config.name,
        userGoal=config.userGoal,
        selectedOutputFormat=config.selectedOutputFormat,
        contextProvided=config.contextProvided,
        constraints_json=constraints_json_str,
        personaDescription=config.personaDescription,
        personaSkipped=config.personaSkipped,
        constructedPrompt=config.constructedPrompt,
        owner_id=owner_id
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

def get_prompt_configurations(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.PromptConfigurationDB]:
    """Retrieves a list of prompt configurations for a specific user."""
    return db.query(models.PromptConfigurationDB).filter(models.PromptConfigurationDB.owner_id == owner_id).offset(skip).limit(limit).all()

def get_prompt_configuration_by_id(db: Session, config_id: int, owner_id: int) -> Optional[models.PromptConfigurationDB]:
    """Retrieves a single prompt configuration by its ID, ensuring it belongs to the specified owner."""
    return db.query(models.PromptConfigurationDB).filter(
        models.PromptConfigurationDB.id == config_id, 
        models.PromptConfigurationDB.owner_id == owner_id
    ).first()

def update_prompt_configuration(
    db: Session, 
    config_id: int, 
    config_update: models.PromptConfigurationCreate,
    owner_id: int
) -> Optional[models.PromptConfigurationDB]:
    """Updates an existing prompt configuration, ensuring it belongs to the specified owner."""
    db_config = get_prompt_configuration_by_id(db, config_id, owner_id)
    if db_config:
        update_data = config_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "constraints":
                setattr(db_config, "constraints_json", json.dumps(value))
            else:
                setattr(db_config, key, value)
        db.commit()
        db.refresh(db_config)
    return db_config

def delete_prompt_configuration(db: Session, config_id: int, owner_id: int) -> Optional[models.PromptConfigurationDB]:
    """Deletes a prompt configuration by its ID, ensuring it belongs to the specified owner."""
    db_config = get_prompt_configuration_by_id(db, config_id, owner_id)
    if db_config:
        db.delete(db_config)
        db.commit()
    return db_config