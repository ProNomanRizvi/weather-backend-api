"""
Pytest configuration.

This file creates a separate database and test client
used by every test.
"""

import os
from app.models.weather import Weather

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import get_db
from app.database.test_database import (
    Base,
    engine,
    TestingSessionLocal,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create the test database before tests
    and remove it afterwards.
    """

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

    if os.path.exists("test_weather.db"):
        os.remove("test_weather.db")


def override_get_db():
    """
    Override the application's database
    dependency with the test database.
    """

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """
    Return a test client.
    """

    return TestClient(app)