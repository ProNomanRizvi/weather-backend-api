"""
Database service for weather records.

This module contains all database operations related
to weather records.
"""

from sqlalchemy.orm import Session

from app.models.weather import Weather
from app.schemas.weather import WeatherCreate, WeatherUpdate


def create_weather(
    db: Session,
    weather: WeatherCreate,
) -> Weather:
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

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return weather_record


def create_weather_from_api(
    db: Session,
    weather_data: dict,
) -> Weather:
    """
    Save weather fetched from OpenWeather.
    """

    weather_record = Weather(**weather_data)

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return weather_record


def get_all_weather(
    db: Session,
):
    """
    Return every weather record.
    """

    return (
        db.query(Weather)
        .order_by(Weather.id.desc())
        .all()
    )


def get_weather_by_id(
    db: Session,
    weather_id: int,
):
    """
    Return one weather record.
    """

    return (
        db.query(Weather)
        .filter(Weather.id == weather_id)
        .first()
    )


def update_weather(
    db: Session,
    weather_record: Weather,
    weather: WeatherUpdate,
):
    """
    Update a weather record.
    """

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


def delete_weather(
    db: Session,
    weather_record: Weather,
):
    """
    Delete a weather record.
    """

    db.delete(weather_record)
    db.commit()