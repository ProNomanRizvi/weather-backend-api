"""
Export service.

Provides functionality for exporting weather
records into different file formats.
"""

import csv

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.models.weather import Weather


def export_weather_csv(
    db: Session,
):
    """
    Export all weather records as a CSV file.
    """

    weather_records = (
        db.query(Weather)
        .order_by(Weather.id.desc())
        .all()
    )

    from io import StringIO

    csv_file = StringIO()

    writer = csv.writer(csv_file)

    # CSV header
    writer.writerow([
        "ID",
        "City",
        "Country",
        "Temperature",
        "Humidity",
        "Pressure",
        "Wind Speed",
        "Weather Condition",
    ])

    # CSV rows
    for record in weather_records:
        writer.writerow([
            record.id,
            record.city,
            record.country,
            record.temperature,
            record.humidity,
            record.pressure,
            record.wind_speed,
            record.weather_condition,
        ])

    csv_file.seek(0)

    return StreamingResponse(
        iter([csv_file.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=weather_data.csv"
        },
    )