# artisan_ai_backend/app/routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, auth, database

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register", response_model=models.User, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_create: models.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user. Hashes the password before saving.
    """
    db_user_with_email = crud.get_user_by_email(db, email=user_create.email)
    if db_user_with_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # CORRECTED: Hashing is now done in the API layer, not the data layer.
    hashed_password = auth.get_password_hash(user_create.password)
    return crud.create_user(db=db, user=user_create, hashed_password=hashed_password)

@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get current logged-in user.
    """
    return current_user