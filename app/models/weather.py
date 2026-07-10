"""
Weather database model.

This table stores weather information fetched from the external API.
Keeping the raw data locally makes it easier to build reports,
export records, or avoid repeated API calls.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Weather(Base):
    """
    Represents a weather record stored in the database.
    """

    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    humidity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pressure: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    wind_speed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    weather_condition: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )