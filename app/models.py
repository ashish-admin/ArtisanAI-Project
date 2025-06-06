# artisan_ai_backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import json

from .database import Base # Assuming your Base is defined in database.py

# --- Pydantic Model for Constraints (Used by PromptConfiguration and LLMRecommendationRequest) ---
class ConstraintsModel(BaseModel):
    length: Optional[str] = None
    tone: Optional[str] = None
    includeKeywords: Optional[List[str]] = None # Changed from Optional[str]
    excludeKeywords: Optional[List[str]] = None # Changed from Optional[str]
    prioritizeQuality: Optional[bool] = True

# --- User Pydantic Models ---
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase): # For potential future use
    password: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase): # For API responses (doesn't include password_hash)
    id: int
    
    class Config:
        from_attributes = True # Pydantic V2 (formerly orm_mode)

class UserInDB(User): # Includes hashed_password, could be used for internal logic if needed
    hashed_password: str


# --- Token Pydantic Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): # Data to be encoded in the JWT
    email: Optional[EmailStr] = None

# --- SQLAlchemy User Model ---
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    prompt_configurations = relationship("PromptConfigurationDB", back_populates="owner")

# --- SQLAlchemy Prompt Configuration Model ---
class PromptConfigurationDB(Base):
    __tablename__ = "prompt_configurations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    userGoal = Column(Text, nullable=False)
    selectedOutputFormat = Column(String, nullable=False)
    contextProvided = Column(Text, nullable=True)
    constraints_json = Column(Text, nullable=True)
    personaDescription = Column(Text, nullable=True)
    personaSkipped = Column(Boolean, default=False)
    constructedPrompt = Column(Text, nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="prompt_configurations")

    @property
    def constraints(self) -> ConstraintsModel:
        if self.constraints_json:
            try:
                data = json.loads(self.constraints_json)
                return ConstraintsModel(**data)
            except json.JSONDecodeError:
                # Consider using proper logging here for production
                print(f"Warning: Failed to decode constraints_json for Config ID {self.id if hasattr(self, 'id') else 'Unknown'}: {self.constraints_json}")
                return ConstraintsModel() # Return default if decoding fails
        return ConstraintsModel() # Return default if no JSON string

# --- Pydantic Prompt Configuration Models ---
class PromptConfigurationBase(BaseModel):
    name: str
    userGoal: str
    selectedOutputFormat: str
    contextProvided: Optional[str] = None
    constraints: ConstraintsModel
    personaDescription: Optional[str] = None
    personaSkipped: bool = False
    constructedPrompt: str

class PromptConfigurationCreate(PromptConfigurationBase):
    pass

class PromptConfiguration(PromptConfigurationBase): # For API responses
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# --- Pydantic Models for LLM Recommendation Service ---
class LLMRecommendationRequest(BaseModel):
    userGoal: str
    selectedOutputFormat: str
    contextProvided: Optional[str] = None
    constraints: ConstraintsModel  # Re-using the existing ConstraintsModel
    personaDescription: Optional[str] = None
    # personaSkipped: bool # Can be inferred if personaDescription is None/empty
    # Optional future fields for more nuanced recommendations:
    # estimatedPromptLengthChars: Optional[int] = None
    # desiredComplexityLevel: Optional[str] = Field(None, pattern="^(simple|intermediate|advanced)$")

class LLMSuggestion(BaseModel):
    llm_name: str
    reason: str
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    # Potential future fields:
    # provider: Optional[str] = None
    # matched_strengths: Optional[List[str]] = None
    # notes_for_llm_choice: Optional[str] = None

class LLMRecommendationResponse(BaseModel):
    suggestions: List[LLMSuggestion]
    notes: Optional[str] = None
    # Optional future fields:
    # estimated_prompt_length_chars: Optional[int] = None

# --- Pydantic Models for Prompt Crafting ---
class PromptCraftRequest(BaseModel):
    userGoal: str
    selectedOutputFormat: str
    contextProvided: Optional[str] = None
    constraints: ConstraintsModel
    personaDescription: Optional[str] = None
    personaSkipped: bool = False

