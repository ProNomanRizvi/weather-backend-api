"""
Tests for weather API endpoints.
"""

from fastapi.testclient import TestClient
import json
from app.main import app

# Test client used to make HTTP requests.
client = TestClient(app)


def test_create_weather():
    """
    Verify a weather record can be created.
    """

    payload = {
        "city": "Lahore",
        "country": "PK",
        "temperature": 32.5,
        "humidity": 60,
        "pressure": 1000,
        "wind_speed": 4.2,
        "weather_condition": "Clear",
    }

    response = client.post(
        "/weather/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["city"] == payload["city"]
    assert data["country"] == payload["country"]
    assert data["temperature"] == payload["temperature"]
    assert data["humidity"] == payload["humidity"]
    assert data["pressure"] == payload["pressure"]
    assert data["wind_speed"] == payload["wind_speed"]
    assert data["weather_condition"] == payload["weather_condition"]

    # Database should generate these values automatically.
    assert "id" in data
    assert "created_at" in data

def test_get_all_weather():
    """
    Verify all weather records can be retrieved.
    """

    response = client.get("/weather/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # There should be at least one record because
    # test_create_weather() inserted one.
    assert len(data) >= 1

    first_record = data[0]

    assert "id" in first_record
    assert "city" in first_record
    assert "country" in first_record
    assert "temperature" in first_record
    assert "humidity" in first_record
    assert "pressure" in first_record
    assert "wind_speed" in first_record
    assert "weather_condition" in first_record
    assert "created_at" in first_record

def test_get_weather_by_id():
    # Create a weather record
    response = client.post(
        "/weather/",
        json={
            "city": "Karachi",
            "country": "PK",
            "temperature": 32.5,
            "humidity": 60,
            "pressure": 1008,
            "wind_speed": 4.2,
            "weather_condition": "Sunny",
        },
    )

    weather = response.json()

    # Retrieve it by ID
    response = client.get(f"/weather/{weather['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather["id"]
    assert data["city"] == "Karachi"
    assert data["country"] == "PK"

def test_update_weather():
    """
    Verify an existing weather record can be updated.
    """

    # Create a weather record first.
    response = client.post(
        "/weather/",
        json={
            "city": "Lahore",
            "country": "PK",
            "temperature": 30.0,
            "humidity": 55,
            "pressure": 1005,
            "wind_speed": 3.5,
            "weather_condition": "Clear",
        },
    )

    weather = response.json()

    # Updated values.
    updated_data = {
        "city": "Islamabad",
        "country": "PK",
        "temperature": 25.5,
        "humidity": 70,
        "pressure": 1012,
        "wind_speed": 2.8,
        "weather_condition": "Clouds",
    }

    # Send update request.
    response = client.put(
        f"/weather/{weather['id']}",
        json=updated_data,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == weather["id"]
    assert data["city"] == "Islamabad"
    assert data["country"] == "PK"
    assert data["temperature"] == 25.5
    assert data["humidity"] == 70
    assert data["pressure"] == 1012
    assert data["wind_speed"] == 2.8
    assert data["weather_condition"] == "Clouds"

def test_delete_weather():
    """
    Verify a weather record can be deleted.
    """

    # Create a weather record.
    response = client.post(
        "/weather/",
        json={
            "city": "Peshawar",
            "country": "PK",
            "temperature": 34.0,
            "humidity": 48,
            "pressure": 1007,
            "wind_speed": 3.1,
            "weather_condition": "Sunny",
        },
    )

    weather = response.json()

    # Delete the record.
    response = client.delete(
        f"/weather/{weather['id']}"
    )

    assert response.status_code == 204

    # Verify the record no longer exists.
    response = client.get(
        f"/weather/{weather['id']}"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Weather record not found."

def test_fetch_and_save_weather():
    """
    Verify live weather data can be fetched
    and stored in the database.
    """

    response = client.post(
        "/weather/fetch/Lahore"
    )

    assert response.status_code == 201

    data = response.json()

    assert data["city"] == "Lahore"
    assert data["country"] == "PK"

    assert "temperature" in data
    assert "humidity" in data
    assert "pressure" in data
    assert "wind_speed" in data
    assert "weather_condition" in data

    assert "id" in data
    assert "created_at" in data

def test_export_weather_csv():
    """
    Verify weather records can be exported as a CSV file.
    """

    response = client.get(
        "/weather/export/csv"
    )

    assert response.status_code == 200

    assert response.headers["content-type"].startswith(
        "text/csv"
    )

    assert "weather_data.csv" in response.headers["content-disposition"]

    content = response.text

    # Verify the CSV contains the expected header.
    assert "City" in content
    assert "Country" in content
    assert "Temperature" in content

def test_export_weather_json():
    """
    Verify weather records can be exported as a JSON file.
    """

    response = client.get(
        "/weather/export/json"
    )

    assert response.status_code == 200

    assert response.headers["content-type"].startswith(
        "application/json"
    )

    content_disposition = response.headers[
        "content-disposition"
    ]

    assert "attachment" in content_disposition
    assert "weather_data.json" in content_disposition

    data = json.loads(response.text)

    assert isinstance(data, list)

    if data:
        weather = data[0]

        assert "id" in weather
        assert "city" in weather
        assert "country" in weather
        assert "temperature" in weather
        assert "humidity" in weather
        assert "pressure" in weather
        assert "wind_speed" in weather
        assert "weather_condition" in weather
        assert "created_at" in weather

def test_weather_not_found():
    """
    Verify requesting a non-existent weather record
    returns a 404 response.
    """

    response = client.get("/weather/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["status_code"] == 404
    assert data["message"] == "Weather record not found."