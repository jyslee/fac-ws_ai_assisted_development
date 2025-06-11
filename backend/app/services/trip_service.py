"""Trip service layer for business logic operations."""

from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlmodel import Session

from app.models.request import TripCreate, TripUpdate
from app.models.response import TripResponse
from app.models.tables import Trip
from app.repositories.trip_repository import TripRepository


class TripService:
    """Service class for Trip business logic operations."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.repository = TripRepository(session)

    async def get_all_trips(self) -> List[TripResponse]:
        """Get all trips from repository and return as response models."""
        trips = self.repository.get_all()
        return [TripResponse.from_trip(trip) for trip in trips]

    async def get_trip_by_id(self, trip_id: int) -> TripResponse:
        """Get a specific trip by ID."""
        trip = self.repository.get_by_id(trip_id)
        if trip is None:
            raise HTTPException(
                status_code=404, detail=f"Trip with id {trip_id} not found"
            )
        return TripResponse.from_trip(trip)

    async def create_trip(self, trip_data: TripCreate) -> TripResponse:
        """Create a new trip from request data."""
        now = datetime.utcnow()

        # Create Trip table model from request data
        trip = Trip(
            name=trip_data.name,
            destination=trip_data.destination,
            start_date=trip_data.start_date,
            end_date=trip_data.end_date,
            notes=trip_data.notes,
            created_at=now,
            updated_at=now,
        )

        # Save to repository
        created_trip = self.repository.create(trip)
        return TripResponse.from_trip(created_trip)

    async def update_trip(self, trip_id: int, updates: TripUpdate) -> TripResponse:
        """Update an existing trip with partial updates."""
        # Get existing trip
        existing_trip = self.repository.get_by_id(trip_id)
        if existing_trip is None:
            raise HTTPException(
                status_code=404, detail=f"Trip with id {trip_id} not found"
            )

        # Apply updates only for provided fields
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_trip, field, value)

        # Update timestamp
        existing_trip.updated_at = datetime.utcnow()

        # Save changes
        updated_trip = self.repository.update(existing_trip)
        return TripResponse.from_trip(updated_trip)

    async def delete_trip(self, trip_id: int) -> None:
        """Delete a trip by ID."""
        deleted = self.repository.delete(trip_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail=f"Trip with id {trip_id} not found"
            )
