# artisan_ai_backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite database URL. 
# For a local file, it will be 'sqlite:///./artisan_ai_be.db'
# This means the database file 'artisan_ai_be.db' will be created in the same directory 
# where you run the uvicorn server (likely the root of your artisan_ai_backend project).
SQLALCHEMY_DATABASE_URL = "sqlite:///./artisan_ai_be.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed only for SQLite.
# It's because SQLite by default only allows one thread to communicate with it,
# and FastAPI, being asynchronous, might use multiple threads for a single request.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of the SessionLocal class will be a database session.
# The class itself hasn't been created yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class to create each of the database models (ORM models)
Base = declarative_base()

# Dependency to get a DB session (will be used in API endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()