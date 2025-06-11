"""Trip API routes for FastAPI application."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.models.request import TripCreate, TripUpdate
from app.models.response import TripResponse
from app.services.trip_service import TripService

router = APIRouter(prefix="/api/trips", tags=["trips"])


def get_trip_service(session: Session = Depends(get_session)) -> TripService:
    """Dependency injection for TripService."""
    return TripService(session)


@router.get("/", response_model=List[TripResponse])
async def get_all_trips(
    trip_service: TripService = Depends(get_trip_service),
) -> List[TripResponse]:
    """Get all trips."""
    return await trip_service.get_all_trips()


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip_data: TripCreate,
    trip_service: TripService = Depends(get_trip_service),
) -> TripResponse:
    """Create a new trip."""
    try:
        return await trip_service.create_trip(trip_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip_by_id(
    trip_id: int,
    trip_service: TripService = Depends(get_trip_service),
) -> TripResponse:
    """Get a specific trip by ID."""
    return await trip_service.get_trip_by_id(trip_id)


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: int,
    updates: TripUpdate,
    trip_service: TripService = Depends(get_trip_service),
) -> TripResponse:
    """Update an existing trip."""
    try:
        return await trip_service.update_trip(trip_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    trip_id: int,
    trip_service: TripService = Depends(get_trip_service),
) -> None:
    """Delete a trip."""
    await trip_service.delete_trip(trip_id)
