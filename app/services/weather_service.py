"""
Weather service.

Handles communication with the external weather API.
Keeping API calls here keeps endpoint logic clean.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = os.getenv("OPENWEATHER_BASE_URL")


def fetch_weather(city: str):
    """
    Fetch current weather for the given city.
    """

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()