"""
Pydantic schemas for weather data.

Schemas define what the API accepts from clients and
what it returns in responses.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherBase(BaseModel):
    """
    Common weather fields shared by multiple schemas.
    """

    city: str
    country: str
    temperature: float
    humidity: int
    pressure: int
    wind_speed: float
    weather_condition: str


class WeatherCreate(WeatherBase):
    """
    Data required to create a weather record.
    """

    pass


class WeatherUpdate(WeatherBase):
    """
    Data required to update a weather record.
    """

    pass


class WeatherResponse(WeatherBase):
    """
    Weather data returned by the API.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)