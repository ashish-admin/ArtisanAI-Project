# backend/app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# The async engine is the entry point to the database.
# future=True enables 2.0 style usage.
# pool_pre_ping=True helps manage connections that may have been closed by the database.
async_engine = create_async_engine(
    settings.DATABASE_URL, 
    future=True,
    echo=False,  # Set to True to see SQL queries in the console
    pool_pre_ping=True
)

# The sessionmaker is a factory for creating new Session objects.
# We configure it to use our async engine and the AsyncSession class.
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    """
    Dependency function that yields a new SQLAlchemy session for each request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()