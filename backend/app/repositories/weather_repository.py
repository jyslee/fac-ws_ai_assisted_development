"""Weather repository for data access layer operations with caching."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from app.models.tables import WeatherCache


class WeatherRepository:
    """Repository class for Weather cache database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_cached_weather(self, location: str) -> Optional[WeatherCache]:
        """Get cached weather data for a location if not expired."""
        statement = select(WeatherCache).where(WeatherCache.location == location)
        weather_cache = self.session.exec(statement).first()

        if weather_cache is None:
            return None

        # Check if cache is expired (30-minute expiry)
        if weather_cache.is_expired:
            # Remove expired cache entry
            self.session.delete(weather_cache)
            self.session.commit()
            return None

        return weather_cache

    def store_weather_cache(self, weather_cache: WeatherCache) -> WeatherCache:
        """Store new weather data in cache."""
        # Check if entry already exists for this location
        existing_cache = self.get_cached_weather(location=weather_cache.location)

        if existing_cache:
            # Update existing cache entry
            existing_cache.temperature = weather_cache.temperature
            existing_cache.condition = weather_cache.condition
            existing_cache.humidity = weather_cache.humidity
            existing_cache.wind_speed = weather_cache.wind_speed
            existing_cache.updated_at = weather_cache.updated_at
            existing_cache.cached_at = datetime.utcnow()

            self.session.add(existing_cache)
            self.session.commit()
            self.session.refresh(existing_cache)
            return existing_cache
        else:
            # Create new cache entry
            self.session.add(weather_cache)
            self.session.commit()
            self.session.refresh(weather_cache)
            return weather_cache

    def cleanup_expired_cache(self) -> int:
        """Remove all expired weather cache entries. Returns count of removed entries."""
        statement = select(WeatherCache)
        all_cached_weather = self.session.exec(statement).all()

        expired_count = 0
        for weather_cache in all_cached_weather:
            if weather_cache.is_expired:
                self.session.delete(weather_cache)
                expired_count += 1

        if expired_count > 0:
            self.session.commit()

        return expired_count

    def clear_location_cache(self, location: str) -> bool:
        """Clear cache for a specific location. Returns True if cache was found and cleared."""
        statement = select(WeatherCache).where(WeatherCache.location == location)
        weather_cache = self.session.exec(statement).first()

        if weather_cache is None:
            return False

        self.session.delete(weather_cache)
        self.session.commit()
        return True

    def get_all_cached_locations(self) -> List[str]:
        """Get list of all currently cached locations (non-expired)."""
        statement = select(WeatherCache)
        all_cached_weather = self.session.exec(statement).all()

        valid_locations = []
        for weather_cache in all_cached_weather:
            if not weather_cache.is_expired:
                valid_locations.append(weather_cache.location)

        return valid_locations

    def exists(self, location: str) -> bool:
        """Check if valid (non-expired) cache exists for a location."""
        cached_weather = self.get_cached_weather(location)
        return cached_weather is not None
