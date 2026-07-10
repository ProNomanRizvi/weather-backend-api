"""
Application entry point.

The FastAPI app is created here and all API routers will be
registered from this file as the project grows.
"""

from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.weather import Weather

app = FastAPI(
    title="Weather Backend API",
    description="Backend service for managing and retrieving weather data.",
    version="1.0.0",
)

# Create database tables during application startup.
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    """
    Simple endpoint to confirm that the server is running.
    """
    return {
        "message": "Weather Backend API is running.",
        "status": "success"
    }