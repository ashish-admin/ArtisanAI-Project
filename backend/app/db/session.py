# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Database Configuration ---
# For our MVP, we will use a simple SQLite database.
# The file 'artisan_ai_be.db' will be created in the root directory.
# The 'connect_args' is recommended for SQLite to prevent issues with single-threaded access.
SQLALCHEMY_DATABASE_URL = "sqlite:///./artisan_ai_be.db"

# The SQLAlchemy engine is the core interface to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# The SessionLocal class is a "session factory". Each instance of SessionLocal
# will be a new database session. This is the standard way to handle sessions
# in FastAPI applications.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependency for FastAPI ---
def get_db():
    """
    A FastAPI dependency that creates and yields a new database session
    for each incoming API request. It ensures the session is always
    closed, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()