"""Trip repository for data access layer operations."""

from typing import List, Optional

from sqlmodel import Session, desc, select

from app.models.tables import Trip


class TripRepository:
    """Repository class for Trip database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_all(self) -> List[Trip]:
        """Get all trips from database."""
        statement = select(Trip).order_by(desc(Trip.created_at))
        trips = self.session.exec(statement).all()
        return list(trips)

    def get_by_id(self, trip_id: int) -> Optional[Trip]:
        """Get a trip by ID."""
        statement = select(Trip).where(Trip.id == trip_id)
        trip = self.session.exec(statement).first()
        return trip

    def create(self, trip: Trip) -> Trip:
        """Create a new trip in database."""
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def update(self, trip: Trip) -> Trip:
        """Update an existing trip in database."""
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def delete(self, trip_id: int) -> bool:
        """Delete a trip by ID. Returns True if deleted, False if not found."""
        trip = self.get_by_id(trip_id)
        if trip is None:
            return False

        self.session.delete(trip)
        self.session.commit()
        return True

    def exists(self, trip_id: int) -> bool:
        """Check if a trip exists by ID."""
        statement = select(Trip.id).where(Trip.id == trip_id)
        result = self.session.exec(statement).first()
        return result is not None
