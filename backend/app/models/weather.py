"""Weather data models with SQLModel and Pydantic validation."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel


class WeatherResponse(SQLModel):
    """Weather response model for API responses."""

    location: str = Field(description="Weather location")
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition description")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(ge=0, description="Wind speed in km/h")
    updated_at: datetime = Field(description="When weather data was last updated")


class WeatherCache(WeatherResponse, table=True):
    """Weather cache model for database storage with 30-minute expiry."""

    id: Optional[int] = Field(default=None, primary_key=True)
    cached_at: datetime = Field(
        default_factory=datetime.utcnow, description="When data was cached"
    )

    @property
    def is_expired(self) -> bool:
        """Check if cached weather data is older than 30 minutes."""
        return (datetime.utcnow() - self.cached_at).total_seconds() > 1800  # 30 minutes


class WeatherAPIResponse(SQLModel):
    """Model for external weather API response parsing."""

    main: dict = Field(description="Main weather data from API")
    weather: List[dict] = Field(description="Weather conditions array")
    wind: dict = Field(description="Wind data from API")
    name: str = Field(description="Location name from API")

    def to_weather_response(self) -> WeatherResponse:
        """Convert API response to our WeatherResponse model."""
        return WeatherResponse(
            location=self.name,
            temperature=round(
                self.main["temp"] - 273.15, 1
            ),  # Convert Kelvin to Celsius
            condition=self.weather[0]["description"].title(),
            humidity=self.main["humidity"],
            wind_speed=round(self.wind.get("speed", 0) * 3.6, 1),  # Convert m/s to km/h
            updated_at=datetime.utcnow(),
        )


class MockWeatherData(SQLModel):
    """Mock weather data for development without API key."""

    @staticmethod
    def generate_mock_weather(location: str) -> WeatherResponse:
        """Generate mock weather data for a given location."""
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
