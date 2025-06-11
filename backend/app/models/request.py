"""Request models for API input validation."""

from datetime import date
from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator


class TripCreate(BaseModel):
    """Trip creation request model."""

    name: str = Field(min_length=1, max_length=100, description="Trip name")
    destination: str = Field(min_length=1, description="Trip destination")
    start_date: date = Field(description="Trip start date")
    end_date: date = Field(description="Trip end date")
    notes: Optional[str] = Field(default=None, max_length=500, description="Trip notes")

    @field_validator("end_date")
    @classmethod
    def validate_end_after_start(cls, end_date: date, info: Any) -> date:
        """Validate that end_date is after start_date."""
        if hasattr(info, "data") and "start_date" in info.data:
            start_date = info.data["start_date"]
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
        return end_date


class TripUpdate(BaseModel):
    """Trip update request model for partial updates."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    destination: Optional[str] = Field(default=None, min_length=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=500)

    @field_validator("end_date")
    @classmethod
    def validate_dates_if_provided(
        cls, end_date: Optional[date], info: Any
    ) -> Optional[date]:
        """Validate dates if both start and end are provided in update."""
        if end_date is not None and hasattr(info, "data") and "start_date" in info.data:
            start_date = info.data["start_date"]
            if start_date is not None and end_date <= start_date:
                raise ValueError("End date must be after start date")
        return end_date


class WeatherAPIRequest(BaseModel):
    """Model for external weather API request parsing."""

    main: dict = Field(description="Main weather data from API")
    weather: List[dict] = Field(description="Weather conditions array")
    wind: dict = Field(description="Wind data from API")
    name: str = Field(description="Location name from API")

    def to_celsius(self, kelvin_temp: float) -> float:
        """Convert Kelvin temperature to Celsius."""
        return round(kelvin_temp - 273.15, 1)

    def to_kmh(self, ms_speed: float) -> float:
        """Convert m/s wind speed to km/h."""
        return round(ms_speed * 3.6, 1)
