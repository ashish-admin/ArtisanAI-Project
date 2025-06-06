# artisan_ai_backend/app/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # For encoding/decoding JWTs
from passlib.context import CryptContext # For password hashing
from pydantic import BaseModel, EmailStr # <--- ENSURE THIS IMPORT IS HERE

from sqlalchemy.orm import Session

# Import models and crud carefully to avoid circular dependencies at top level
# We'll import crud locally within functions where needed if it causes issues.
from . import models 
from . import database # For database.get_db

# --- Configuration ---
# IMPORTANT: Generate a strong, random string for SECRET_KEY and store it securely, 
# preferably as an environment variable, not hardcoded in production.
# For example, you can generate one using Python: import os; os.urandom(32).hex()
SECRET_KEY = "your-super-secret-and-strong-key-please-change-me" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token validity period (e.g., 60 minutes)

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- JWT Token Handling ---
# This scheme will expect a token to be sent in the Authorization header as "Bearer <token>"
# tokenUrl points to our login endpoint which will generate the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") 

# Pydantic model for data inside the JWT token (subject/email)
# This was the class causing 'BaseModel not defined' if pydantic import was missing
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependency to Get Current User ---
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db) # Get DB session
) -> models.UserDB: # Returns the SQLAlchemy UserDB model
    # Import crud here to avoid circular import issues at the module's top level
    from . import crud 
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_from_token: Optional[str] = payload.get("sub") # "sub" is the standard JWT claim for subject
        if email_from_token is None:
            raise credentials_exception
        # Validate email format from token data
        token_data = TokenData(email=EmailStr(email_from_token)) 
    except JWTError: # If token is invalid (e.g., expired, malformed)
        raise credentials_exception
    except ValueError: # Catches Pydantic validation error for EmailStr if email_from_token is not valid
        raise credentials_exception

    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: models.UserDB = Depends(get_current_user)
) -> models.User: # Returns the Pydantic User model for API responses
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    # Convert UserDB (SQLAlchemy) to User (Pydantic) for API response consistency
    return models.User.model_validate(current_user) # Pydantic V2