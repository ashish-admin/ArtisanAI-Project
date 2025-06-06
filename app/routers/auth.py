# artisan_ai_backend/app/routers/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session

# Use relative imports to go up one level to the 'app' directory
# then access modules like crud, models, auth (for its functions), database
from .. import crud 
from .. import models
from .. import auth # For auth utility functions like verify_password, create_access_token
from .. import database # For database.get_db

router = APIRouter(
    prefix="/api/v1/auth", 
    tags=["Authentication"], 
)

@router.post("/register", response_model=models.User, status_code=status.HTTP_201_CREATED)
async def register_new_user(user_create: models.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user.
    """
    db_user_with_email = crud.get_user_by_email(db, email=user_create.email)
    if db_user_with_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        # The create_user function in crud.py now handles password hashing
        created_user = crud.create_user(db=db, user=user_create)
        return created_user
    except Exception as e:
        print(f"Error during user registration: {e}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Could not create user.")


@router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    FastAPI's OAuth2PasswordRequestForm sends 'username' and 'password'.
    We'll use 'username' as the email.
    """
    user = crud.get_user_by_email(db, email=form_data.username) # form_data.username is the email
    
    # Use auth.verify_password from the imported auth module
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    # Use auth.ACCESS_TOKEN_EXPIRE_MINUTES and auth.create_access_token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get current logged-in user.
    """
    return current_user