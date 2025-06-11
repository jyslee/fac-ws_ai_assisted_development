"""Response models for API output formatting."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from .tables import Trip


class TripResponse(BaseModel):
    """Trip response model for API responses."""

    id: int
    name: str = Field(description="Trip name")
    destination: str = Field(description="Trip destination")
    start_date: date = Field(description="Trip start date")
    end_date: date = Field(description="Trip end date")
    notes: Optional[str] = Field(description="Trip notes")
    created_at: datetime
    updated_at: datetime
    duration_days: int

    @classmethod
    def from_trip(cls, trip: Trip) -> "TripResponse":
        """Create TripResponse from Trip table model."""
        return cls(
            id=trip.id or 0,  # Handle None case for type safety
            name=trip.name,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            notes=trip.notes,
            created_at=trip.created_at,
            updated_at=trip.updated_at,
            duration_days=trip.duration_days,
        )


class WeatherResponse(BaseModel):
    """Weather response model for API responses."""

    location: str = Field(description="Weather location")
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition description")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(ge=0, description="Wind speed in km/h")
    updated_at: datetime = Field(description="When weather data was last updated")


class MockWeatherResponse(BaseModel):
    """Mock weather response for development without API key."""

    @staticmethod
    def generate_mock_weather(location: str) -> WeatherResponse:
        """Generate consistent mock weather data for a given location."""
        # Simple mock data based on location hash for consistency
        location_hash = hash(location.lower()) % 100

        return WeatherResponse(
            location=location,
            temperature=15 + (location_hash % 25),  # 15-40°C
            condition=["Sunny", "Partly Cloudy", "Cloudy", "Rainy"][location_hash % 4],
            humidity=40 + (location_hash % 50),  # 40-90%
            wind_speed=5 + (location_hash % 20),  # 5-25 km/h
            updated_at=datetime.utcnow(),
        )
