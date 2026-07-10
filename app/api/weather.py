"""
Weather API endpoints.

This module contains endpoints for creating and retrieving
weather records stored in the database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
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

    # Add the new record to the current session.
    db.add(weather_record)

    # Save changes to the database.
    db.commit()

    # Reload the object so generated values are available.
    db.refresh(weather_record)

    return weather_record


@router.get(
    "/",
    response_model=list[WeatherResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_weather(
    db: Session = Depends(get_db),
):
    """
    Return all stored weather records.

    The newest records are returned first.
    """

    weather_records = (
        db.query(Weather)
        .order_by(Weather.id.desc())
        .all()
    )

    return weather_records


@router.get(
    "/{weather_id}",
    response_model=WeatherResponse,
    status_code=status.HTTP_200_OK,
)
def get_weather(
    weather_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single weather record by its ID.
    """

    weather_record = (
        db.query(Weather)
        .filter(Weather.id == weather_id)
        .first()
    )

    if weather_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found.",
        )

    return weather_record