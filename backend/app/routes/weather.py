"""Weather API routes for FastAPI application."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session

from app.database import get_session
from app.models.response import WeatherResponse
from app.services.trip_service import TripService
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api", tags=["weather"])


def get_weather_service(session: Session = Depends(get_session)) -> WeatherService:
    """Dependency injection for WeatherService."""
    return WeatherService(session)


def get_trip_service(session: Session = Depends(get_session)) -> TripService:
    """Dependency injection for TripService."""
    return TripService(session)


@router.get("/weather/{location}", response_model=WeatherResponse)
async def get_weather_for_location(
    location: str = Path(..., description="Location name (e.g., 'Paris, France')"),
    weather_service: WeatherService = Depends(get_weather_service),
) -> WeatherResponse:
    """Get current weather for a specific location."""
    if not location or not location.strip():
        raise HTTPException(status_code=400, detail="Location cannot be empty")

    return await weather_service.get_weather_for_location(location)


@router.get("/trips/{trip_id}/weather", response_model=WeatherResponse)
async def get_weather_for_trip(
    trip_id: int = Path(..., description="Trip ID"),
    weather_service: WeatherService = Depends(get_weather_service),
    trip_service: TripService = Depends(get_trip_service),
) -> WeatherResponse:
    """Get current weather for a trip's destination."""
    # First get the trip to retrieve the destination
    trip = await trip_service.get_trip_by_id(trip_id)

    # Then get weather for that destination
    return await weather_service.get_weather_for_location(trip.destination)


@router.get("/weather", response_model=List[str])
async def get_cached_weather_locations(
    weather_service: WeatherService = Depends(get_weather_service),
) -> List[str]:
    """Get list of currently cached weather locations."""
    return weather_service.get_cached_locations()


@router.delete("/weather/{location}/cache")
async def clear_weather_cache_for_location(
    location: str = Path(..., description="Location name to clear from cache"),
    weather_service: WeatherService = Depends(get_weather_service),
) -> dict:
    """Clear weather cache for a specific location."""
    if not location or not location.strip():
        raise HTTPException(status_code=400, detail="Location cannot be empty")

    cleared = weather_service.clear_cache_for_location(location.strip())

    if cleared:
        return {"message": f"Cache cleared for location: {location}"}
    else:
        return {"message": f"No cache found for location: {location}"}


@router.delete("/weather/cache/expired")
async def cleanup_expired_weather_cache(
    weather_service: WeatherService = Depends(get_weather_service),
) -> dict:
    """Clean up all expired weather cache entries."""
    cleaned_count = weather_service.cleanup_expired_cache()
    return {"message": f"Cleaned up {cleaned_count} expired cache entries"}
