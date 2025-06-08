app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api import deps
from app.core import config
from app.db import crud
from app.schemas import token as token_schema
from app.schemas import user as user_schema
from app.services import security

Create a new API router for authentication endpoints
router = APIRouter()

@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def register_new_user(
*,
db: Session = Depends(deps.get_db),
new_user: user_schema.UserCreate,
) -> Any:
"""
Handles new user registration.
Hashes the password before storing it in the database.
"""
# Check if a user with this email already exists
user = crud.get_user_by_email(db, email=new_user.email)
if user:
raise HTTPException(
status_code=400,
detail="A user with this email already exists in the system.",
)

# Hash the password and create the user
hashed_password = security.get_password_hash(new_user.password)
user = crud.create_user(db=db, user=new_user, hashed_password=hashed_password)
return user

@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
"""
OAuth2 compatible token login, get an access token for future requests.
The client sends 'username' and 'password' as form data.
"""
# Authenticate the user
user = crud.get_user_by_email(db, email=form_data.username)
if not user or not security.verify_password(form_data.password, user.hashed_password):
raise HTTPException(
status_code=status.HTTP_401_UNAUTHORIZED,
detail="Incorrect email or password",
headers={"WWW-Authenticate": "Bearer"},
)
elif not user.is_active:
raise HTTPException(status_code=400, detail="Inactive user")

# Create and return the access token
access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
access_token = security.create_access_token(
    subject=user.email, expires_delta=access_token_expires
)
return {
    "access_token": access_token,
    "token_type": "bearer",
}

@router.get("/users/me", response_model=user_schema.User)
def read_current_user(
current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
"""
Fetch the current logged-in user.
This is a protected endpoint that requires a valid token.
"""
return current_user