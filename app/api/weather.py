"""
Weather API endpoints.

This module contains endpoints responsible for creating
and retrieving weather records.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.weather import Weather
from app.schemas.weather import WeatherCreate, WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.post(
    "/",
    response_model=WeatherResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_weather(
    weather: WeatherCreate,
    db: Session = Depends(get_db),
):
    """
    Save a new weather record.
    """

    weather_record = Weather(
        city=weather.city,
        country=weather.country,
        temperature=weather.temperature,
        humidity=weather.humidity,
        pressure=weather.pressure,
        wind_speed=weather.wind_speed,
        weather_condition=weather.weather_condition,
    )

    # Add the new object to the current database session.
    db.add(weather_record)

    # Persist the changes.
    db.commit()

    # Refresh so auto-generated values (id, timestamps) are available.
    db.refresh(weather_record)

    return weather_record