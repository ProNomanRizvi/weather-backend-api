"""
Database configuration for the Weather Backend API.

This module is responsible for:

- Creating the SQLite database connection
- Creating the SQLAlchemy engine
- Creating database sessions
- Providing the Base class for all models

Keeping database-related code in one place makes the project
cleaner and allows us to switch to another database (like PostgreSQL)
with minimal changes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite database file.
# The file will be created automatically if it doesn't exist.
DATABASE_URL = "sqlite:///weather.db"

# Create the SQLAlchemy engine.
# 'check_same_thread=False' allows SQLite to work correctly with FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create a session factory.
# Every request will use its own database session.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Every model (Weather, User, etc.) will inherit from this class.
    """
    pass


def get_db():
    """
    Yield a database session.

    FastAPI automatically closes the session after the request
    finishes, even if an exception occurs.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()