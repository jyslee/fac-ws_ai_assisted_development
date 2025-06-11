"""Models package with organized structure."""

# Database tables
# Request models
from .request import TripCreate, TripUpdate, WeatherAPIRequest

# Response models
from .response import MockWeatherResponse, TripResponse, WeatherResponse
from .tables import Trip, WeatherCache

__all__ = [
    # Tables
    "Trip",
    "WeatherCache",
    # Requests
    "TripCreate",
    "TripUpdate",
    "WeatherAPIRequest",
    # Responses
    "TripResponse",
    "WeatherResponse",
    "MockWeatherResponse",
]
