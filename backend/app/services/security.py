# app/services/security.py
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import JWT_SECRET_KEY

# --- Configuration ---
# The algorithm used for signing the JWT. HS256 is a standard choice.
ALGORITHM = "HS256"
# The default expiration time for access tokens.
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Password Hashing Setup ---
# We use passlib for robust password hashing.
# By specifying "bcrypt", we ensure we're using a strong, widely-used algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    :param password: The plain-text password to hash.
    :return: The resulting hashed password string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against its hashed version.

    :param plain_password: The plain-text password from the user's login attempt.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Token Creation ---
def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    Creates a new JWT access token.

    :param subject: The subject of the token, typically the user's ID or email.
    :param expires_delta: Optional override for the token's expiration time.
    :return: The encoded JWT access token as a string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # The JWT_SECRET_KEY is imported from our central config module.
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt