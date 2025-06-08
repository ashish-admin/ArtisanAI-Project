# app/db/base.py
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# The declarative_base() function returns a new base class from which
# all mapped classes should inherit. This is the central point for
# SQLAlchemy's ORM mapping.
Base = declarative_base()

# --- SQLAlchemy ORM Models ---
# These classes define the structure of our database tables.

class User(Base):
    """
    Represents the 'users' table in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # This creates the one-to-many relationship.
    # The 'back_populates' argument links it to the corresponding
    # relationship on the Project model.
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    """
    Represents a user's writing project and its associated critique parameters.
    This replaces the old 'PromptConfigurationDB'.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    
    # The user's original text for critique
    writing_text = Column(Text, nullable=False)
    
    # Critique parameters
    critique_goal = Column(String, nullable=False) # e.g., "Critique plot pacing"
    critique_persona = Column(String, nullable=True) # e.g., "Professional book editor"
    
    # The final AI-generated critique
    critique_result_text = Column(Text, nullable=True)
    
    # Foreign key to link this project to a user
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Establishes the many-to-one relationship back to the User model
    owner = relationship("User", back_populates="projects")