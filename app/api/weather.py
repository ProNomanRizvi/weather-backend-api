"""
Weather API endpoints.

This module contains endpoints for creating, retrieving,
updating, deleting, and fetching live weather data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from requests.exceptions import HTTPError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.weather import (
    WeatherCreate,
    WeatherResponse,
    WeatherUpdate,
)
from app.services.weather_crud import (
    create_weather as create_weather_record,
    create_weather_from_api,
    delete_weather as delete_weather_record,
    get_all_weather,
    get_weather_by_id,
    update_weather as update_weather_record,
)
from app.services.weather_service import fetch_weather
from app.services.export_service import (
    export_weather_csv,
    export_weather_json,
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

    return create_weather_record(
        db,
        weather,
    )


@router.get(
    "/",
    response_model=list[WeatherResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_weather_endpoint(
    db: Session = Depends(get_db),
):
    """
    Return all stored weather records.
    """

    return get_all_weather(db)

@router.get(
    "/export/csv",
    summary="Export weather records as CSV",
)
def export_weather_csv_endpoint(
    db: Session = Depends(get_db),
):
    """
    Export all weather records as a CSV file.
    """

    return export_weather_csv(db)

@router.get(
    "/export/json",
    summary="Export weather records as JSON",
)
def export_weather_json_endpoint(
    db: Session = Depends(get_db),
):
    """
    Export all weather records as a JSON file.
    """

    return export_weather_json(db)

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
    Return a weather record by its ID.
    """

    weather_record = get_weather_by_id(
        db,
        weather_id,
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

    weather_record = get_weather_by_id(
        db,
        weather_id,
    )

    if weather_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found.",
        )

    return update_weather_record(
        db,
        weather_record,
        weather,
    )


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

    weather_record = get_weather_by_id(
        db,
        weather_id,
    )

    if weather_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found.",
        )

    delete_weather_record(
        db,
        weather_record,
    )

    return None


@router.post(
    "/fetch/{city}",
    response_model=WeatherResponse,
    status_code=status.HTTP_201_CREATED,
)
def fetch_and_save_weather(
    city: str,
    db: Session = Depends(get_db),
):
    """
    Fetch live weather from OpenWeather,
    save it to the database,
    and return the stored record.
    """

    try:
        weather_data = fetch_weather(city)

    except HTTPError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City '{city}' was not found.",
        )

    return create_weather_from_api(
        db,
        weather_data,
    )