pp/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

--- Shared Base Schema ---
Contains common attributes for a user.
class UserBase(BaseModel):
"""
Base Pydantic model for User. Defines common attributes.
EmailStr type provides automatic email validation.
"""
email: EmailStr
is_active: bool = True

--- Schemas for Specific Use Cases ---
class UserCreate(UserBase):
"""
Schema for creating a new user. Inherits from UserBase and adds the password.
This is used as the request body for the /register endpoint.
"""
password: str

class UserUpdate(BaseModel):
"""
Schema for updating an existing user. All fields are optional.
This allows for partial updates (e.g., only changing the password or active status).
"""
email: Optional[EmailStr] = None
password: Optional[str] = None
is_active: Optional[bool] = None

class User(UserBase):
"""
Schema for returning a user in an API response.
It inherits from UserBase and adds the user's ID.
Crucially, it does NOT include the hashed_password.
"""
id: int

class Config:
    """
    Pydantic V2 configuration to enable ORM mode (now from_attributes).
    This allows the Pydantic model to be created directly from a
    SQLAlchemy model instance (e.g., our db.User object).
    """
    from_attributes = True
