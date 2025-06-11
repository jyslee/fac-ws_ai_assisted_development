"""Trip data models with SQLModel and Pydantic validation."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TripBase(SQLModel):
    """Base Trip model with shared fields."""

    name: str = Field(min_length=1, max_length=100, description="Trip name")
    destination: str = Field(min_length=1, description="Trip destination")
    start_date: date = Field(description="Trip start date")
    end_date: date = Field(description="Trip end date")
    notes: Optional[str] = Field(default=None, max_length=500, description="Trip notes")

    def validate_dates(self) -> None:
        """Validate that end_date is after start_date."""
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")


class Trip(TripBase, table=True):
    """Trip database model with auto-generated fields."""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def duration_days(self) -> int:
        """Calculate trip duration in days."""
        return (self.end_date - self.start_date).days


class TripCreate(TripBase):
    """Trip creation model for API requests."""

    def model_post_init(self, __context: None) -> None:
        """Validate dates after model creation."""
        self.validate_dates()


class TripUpdate(SQLModel):
    """Trip update model for partial updates."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    destination: Optional[str] = Field(default=None, min_length=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=500)

    def validate_dates(self, current_trip: Trip) -> None:
        """Validate updated dates against current trip data."""
        start = (
            self.start_date if self.start_date is not None else current_trip.start_date
        )
        end = self.end_date if self.end_date is not None else current_trip.end_date

        if end <= start:
            raise ValueError("End date must be after start date")


class TripRead(TripBase):
    """Trip read model for API responses."""

    id: int
    created_at: datetime
    updated_at: datetime
    duration_days: int

    @classmethod
    def from_trip(cls, trip: Trip) -> "TripRead":
        """Create TripRead from Trip model."""
        return cls(
            id=trip.id,
            name=trip.name,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            notes=trip.notes,
            created_at=trip.created_at,
            updated_at=trip.updated_at,
            duration_days=trip.duration_days,
        )
