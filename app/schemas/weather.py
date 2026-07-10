"""
Pydantic schemas for weather data.

Schemas define what the API accepts from clients and
what it returns in responses. They help validate input
before it reaches the database.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherCreate(BaseModel):
    """
    Data required to create a weather record.
    """

    city: str
    country: str
    temperature: float
    humidity: int
    pressure: int
    wind_speed: float
    weather_condition: str


class WeatherResponse(BaseModel):
    """
    Weather data returned by the API.
    """

    id: int
    city: str
    country: str
    temperature: float
    humidity: int
    pressure: int
    wind_speed: float
    weather_condition: str
    created_at: datetime

    # Allow Pydantic to read SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)