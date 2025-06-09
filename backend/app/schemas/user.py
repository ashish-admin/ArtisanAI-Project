# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
import datetime

# Schema for creating a new user.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for reading a user from the database.
# Includes the hashed_password.
class UserInDB(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True # Changed from orm_mode

# Schema for returning user information via the API.
# Excludes the hashed_password for security.
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True # Changed from orm_mode