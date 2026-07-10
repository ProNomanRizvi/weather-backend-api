"""
Database configuration used only for automated tests.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base

# Separate database used during testing.
TEST_DATABASE_URL = "sqlite:///./test_weather.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_test_db():
    """
    Yield a database session for tests.
    """

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()