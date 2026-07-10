"""
Weather API endpoints.

This module contains endpoints for creating, retrieving,
updating, and deleting weather records.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.weather import Weather
from app.schemas.weather import (
    WeatherCreate,
    WeatherResponse,
    WeatherUpdate,
)

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

    # Refresh the object so generated values are available.
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

    The newest records appear first.
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


@router.put(
    "/{weather_id}",
    response_model=WeatherResponse,
)
def update_weather(
    weather_id: int,
    weather: WeatherUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing weather record.
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

    # Update editable fields.
    weather_record.city = weather.city
    weather_record.country = weather.country
    weather_record.temperature = weather.temperature
    weather_record.humidity = weather.humidity
    weather_record.pressure = weather.pressure
    weather_record.wind_speed = weather.wind_speed
    weather_record.weather_condition = weather.weather_condition

    db.commit()
    db.refresh(weather_record)

    return weather_record


@router.delete(
    "/{weather_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_weather(
    weather_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a weather record.
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

    db.delete(weather_record)
    db.commit()

    return None