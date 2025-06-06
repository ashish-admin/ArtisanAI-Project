# artisan_ai_backend/app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from typing import List, Optional

from . import models
# 'auth' is imported locally in create_user where needed

# --- User CRUD ---
def get_user_by_id(db: Session, user_id: int) -> Optional[models.UserDB]:
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.UserDB]:
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def create_user(db: Session, user: models.UserCreate) -> models.UserDB:
    from . import auth # <--- Localized import of auth here
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.UserDB(email=user.email, hashed_password=hashed_password, is_active=True)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError: 
        db.rollback()
        raise 
    return db_user

# --- Prompt Configuration CRUD (Modified for Ownership) ---
def create_prompt_configuration(db: Session, config: models.PromptConfigurationCreate, owner_id: int) -> models.PromptConfigurationDB:
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
    # No try-except here for IntegrityError on config name, as it's handled in the router
    db.add(db_config)
    db.commit() 
    db.refresh(db_config)
    return db_config

def get_prompt_configurations(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.PromptConfigurationDB]:
    return db.query(models.PromptConfigurationDB).filter(models.PromptConfigurationDB.owner_id == owner_id).offset(skip).limit(limit).all()

def get_prompt_configuration_by_id(db: Session, config_id: int, owner_id: int) -> Optional[models.PromptConfigurationDB]:
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
    db_config = db.query(models.PromptConfigurationDB).filter(
        models.PromptConfigurationDB.id == config_id,
        models.PromptConfigurationDB.owner_id == owner_id
    ).first()
    
    if db_config:
        db_config.name = config_update.name
        db_config.userGoal = config_update.userGoal
        db_config.selectedOutputFormat = config_update.selectedOutputFormat
        db_config.contextProvided = config_update.contextProvided
        db_config.constraints_json = config_update.constraints.model_dump_json()
        db_config.personaDescription = config_update.personaDescription
        db_config.personaSkipped = config_update.personaSkipped
        db_config.constructedPrompt = config_update.constructedPrompt
        
        db.commit() 
        db.refresh(db_config)
    return db_config

def delete_prompt_configuration(db: Session, config_id: int, owner_id: int) -> Optional[models.PromptConfigurationDB]:
    db_config = db.query(models.PromptConfigurationDB).filter(
        models.PromptConfigurationDB.id == config_id,
        models.PromptConfigurationDB.owner_id == owner_id
    ).first()
    if db_config:
        db.delete(db_config)
        db.commit()
    return db_config