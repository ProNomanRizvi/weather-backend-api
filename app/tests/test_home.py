"""
Tests for the application's home endpoint.
"""


def test_home(client):
    """
    Verify the home endpoint is reachable.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Weather Backend API is running.",
        "status": "success",
    }