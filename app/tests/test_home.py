"""
Tests for the application's home endpoint.
"""

from fastapi.testclient import TestClient

from app.main import app

# Create a test client for the FastAPI application.
client = TestClient(app)


def test_home():
    """
    Verify the home endpoint is reachable.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Weather Backend API is running.",
        "status": "success",
    }