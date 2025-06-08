# artisan_ai_backend/app/routers/configurations.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import traceback
from typing import List

from .. import crud, models, database, auth # Added auth import

router = APIRouter(
    prefix="/api/v1/configurations",
    tags=["Prompt Configurations"],
    dependencies=[Depends(auth.get_current_active_user)] # Protect all routes in this router
)

@router.post("/", response_model=models.PromptConfiguration, status_code=201)
async def create_user_prompt_configuration( # Renamed for clarity
    config_create: models.PromptConfigurationCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print(f">>> Endpoint: create_user_prompt_configuration called by User ID: {current_user.id}")
    try:
        created_config = crud.create_prompt_configuration(db=db, config=config_create, owner_id=current_user.id)
        return created_config
    except IntegrityError:
        db.rollback() 
        error_detail = f"Failed to create configuration. A configuration with this name ('{config_create.name}') might already exist for your account, or another unique constraint was violated."
        # Note: Global name uniqueness is still in effect by DB model.
        # If name should be unique per user, DB schema & this error handling should be refined.
        print(f"!!! IntegrityError by User ID {current_user.id}: {error_detail}")
        raise HTTPException(status_code=409, detail=error_detail)
    except Exception:
        db.rollback()
        print(f"!!! An unexpected error occurred for User ID {current_user.id} during config creation !!!")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An unexpected internal error occurred.")

@router.get("/", response_model=List[models.PromptConfiguration])
async def read_user_prompt_configurations( # Renamed for clarity
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print(f">>> Endpoint: read_user_prompt_configurations called by User ID: {current_user.id}")
    configurations = crud.get_prompt_configurations(db, owner_id=current_user.id, skip=skip, limit=limit)
    return configurations

@router.get("/{config_id}", response_model=models.PromptConfiguration)
async def read_single_user_prompt_configuration( # Renamed for clarity
    config_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print(f">>> Endpoint: read_single_user_prompt_configuration called by User ID: {current_user.id} for config_id: {config_id}")
    db_config = crud.get_prompt_configuration_by_id(db, config_id=config_id, owner_id=current_user.id)
    if db_config is None:
        raise HTTPException(status_code=404, detail=f"Prompt Configuration with ID {config_id} not found for your account.")
    return db_config

@router.put("/{config_id}", response_model=models.PromptConfiguration)
async def update_user_prompt_configuration( # Renamed for clarity
    config_id: int, 
    config_update: models.PromptConfigurationCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print(f">>> Endpoint: update_user_prompt_configuration by User ID {current_user.id} for config_id: {config_id}")
    try:
        updated_config = crud.update_prompt_configuration(db=db, config_id=config_id, config_update=config_update, owner_id=current_user.id)
        if updated_config is None:
            raise HTTPException(status_code=404, detail=f"Prompt Configuration with ID {config_id} not found for your account.")
        return updated_config
    except IntegrityError: 
        db.rollback()
        error_detail = f"Failed to update. Another configuration with the name '{config_update.name}' might already exist for your account."
        # See note on global vs per-user name uniqueness in POST endpoint.
        print(f"!!! IntegrityError during update by User ID {current_user.id}: {error_detail}")
        raise HTTPException(status_code=409, detail=error_detail)
    except Exception:
        db.rollback()
        print(f"!!! An unexpected error occurred during update for config_id {config_id} by User ID {current_user.id} !!!")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="An unexpected internal error occurred during update.")

@router.delete("/{config_id}", status_code=204) 
async def delete_user_prompt_configuration( # Renamed for clarity
    config_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    print(f">>> Endpoint: delete_user_prompt_configuration by User ID {current_user.id} for config_id: {config_id}")
    deleted_config = crud.delete_prompt_configuration(db, config_id=config_id, owner_id=current_user.id)
    if deleted_config is None:
        raise HTTPException(status_code=404, detail=f"Prompt Configuration with ID {config_id} not found for your account.")
    return Response(status_code=204)