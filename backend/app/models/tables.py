"""Database table models with SQLModel."""

from datetime import date, datetime
from typing import Any, Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Trip(SQLModel, table=True):
    """Trip database table model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100, description="Trip name")
    destination: str = Field(min_length=1, description="Trip destination")
    start_date: date = Field(description="Trip start date")
    end_date: date = Field(description="Trip end date")
    notes: Optional[str] = Field(default=None, max_length=500, description="Trip notes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("end_date")
    @classmethod
    def validate_end_after_start(cls, end_date: date, info: Any) -> date:
        """Validate that end_date is after start_date."""
        if hasattr(info, "data") and "start_date" in info.data:
            start_date = info.data["start_date"]
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
        return end_date

    @property
    def duration_days(self) -> int:
        """Calculate trip duration in days."""
        return (self.end_date - self.start_date).days


class WeatherCache(SQLModel, table=True):
    """Weather cache database table model with 30-minute expiry."""

    id: Optional[int] = Field(default=None, primary_key=True)
    location: str = Field(description="Weather location")
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition description")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(ge=0, description="Wind speed in km/h")
    updated_at: datetime = Field(description="When weather data was last updated")
    cached_at: datetime = Field(
        default_factory=datetime.utcnow, description="When data was cached"
    )

    @property
    def is_expired(self) -> bool:
        """Check if cached weather data is older than 30 minutes."""
        return (datetime.utcnow() - self.cached_at).total_seconds() > 1800  # 30 minutes
