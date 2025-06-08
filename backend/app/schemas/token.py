# app/schemas/token.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    """
    Pydantic schema for the API response when a user successfully logs in.
    This defines the shape of the JSON that will be sent to the client.
    """
    access_token: str
    token_type: str = "bearer"  # Default to "bearer" as per OAuth2 standard


class TokenData(BaseModel):
    """
    Pydantic schema for the data encoded within the JWT access token.
    This helps us validate the payload after decoding a token.
    """
    email: Optional[EmailStr] = None
