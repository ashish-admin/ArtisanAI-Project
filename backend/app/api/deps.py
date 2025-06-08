# app/api/deps.py
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import config
from app.db import crud
from app.db.base import User
from app.db.session import SessionLocal
from app.schemas.token import TokenData

# This defines the security scheme. It tells FastAPI that the token should be
# expected in the Authorization header as a Bearer token. The tokenUrl points
# to the endpoint where clients can get a token.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.API_V1_STR}/auth/token"
)


def get_db() -> Generator:
    """
    A FastAPI dependency that creates and yields a new database session
    for each incoming API request. It ensures the session is always
    closed, even if an error occurs.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency to get the current user from a JWT token.
    Decodes the token, validates it, and fetches the user from the database.
    """
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        # Pydantic's validation will ensure the email is in the correct format
        token_data = TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    if token_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, user identifier not found in token.",
        )
    
    user = crud.get_user_by_email(db, email=token_data.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    A dependency that builds on get_current_user to ensure the user is active.
    This is the dependency that most protected endpoints will use.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user