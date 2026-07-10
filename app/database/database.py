"""
Database configuration.

This module creates the database engine and session factory.
Keeping everything here makes it easy to switch databases later
without touching the rest of the project.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///weather.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class that every database model will inherit.
    """
    pass


def get_db():
    """
    Provide a database session for each request.

    The session is always closed after the request finishes,
    even if an exception occurs.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()