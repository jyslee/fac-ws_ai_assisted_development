"""Weather service layer for business logic and external API integration."""

from datetime import datetime
import os
from typing import List

from fastapi import HTTPException
import httpx
from sqlmodel import Session

from app.models.request import WeatherAPIRequest
from app.models.response import MockWeatherResponse, WeatherResponse
from app.models.tables import WeatherCache
from app.repositories.weather_repository import WeatherRepository


class WeatherService:
    """Service class for weather operations with external API integration."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.weather_repository = WeatherRepository(session)
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.api_base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather_for_location(self, location: str) -> WeatherResponse:
        """Get weather data for a location with cache-first strategy."""
        if not location or not location.strip():
            raise HTTPException(status_code=400, detail="Location cannot be empty")

        location = location.strip()

        # Try cache first (30-minute expiry built into repository)
        cached_weather = self.weather_repository.get_cached_weather(location)
        if cached_weather:
            return WeatherResponse(
                location=cached_weather.location,
                temperature=cached_weather.temperature,
                condition=cached_weather.condition,
                humidity=cached_weather.humidity,
                wind_speed=cached_weather.wind_speed,
                updated_at=cached_weather.updated_at,
            )

        # Cache miss - fetch from external API or use mock data
        try:
            weather_response = await self._fetch_weather_from_api(location)
        except Exception:
            # Fallback to mock data for development/API failures
            weather_response = MockWeatherResponse.generate_mock_weather(location)

        # Store in cache for future requests
        weather_cache = WeatherCache(
            location=weather_response.location,
            temperature=weather_response.temperature,
            condition=weather_response.condition,
            humidity=weather_response.humidity,
            wind_speed=weather_response.wind_speed,
            updated_at=weather_response.updated_at,
            cached_at=datetime.utcnow(),
        )

        self.weather_repository.store_weather_cache(weather_cache)

        return weather_response

    async def _fetch_weather_from_api(self, location: str) -> WeatherResponse:
        """Fetch weather data from OpenWeatherMap API."""
        if not self.api_key:
            raise ValueError("Weather API key not configured")

        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric",  # Get Celsius directly
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(self.api_base_url, params=params)
                response.raise_for_status()
            except httpx.TimeoutException as e:
                raise HTTPException(
                    status_code=504, detail="Weather service timeout"
                ) from e
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=404, detail=f"Location '{location}' not found"
                    ) from e
                elif e.response.status_code == 401:
                    raise HTTPException(
                        status_code=503, detail="Weather service authentication failed"
                    ) from e
                else:
                    raise HTTPException(
                        status_code=503, detail="Weather service unavailable"
                    ) from e
            except Exception as e:
                raise HTTPException(
                    status_code=503, detail=f"Weather service error: {str(e)}"
                ) from e

        try:
            api_data = response.json()
            weather_request = WeatherAPIRequest(**api_data)

            return WeatherResponse(
                location=weather_request.name,
                temperature=weather_request.main["temp"],  # Already in Celsius
                condition=weather_request.weather[0]["description"].title(),
                humidity=weather_request.main["humidity"],
                wind_speed=weather_request.to_kmh(weather_request.wind.get("speed", 0)),
                updated_at=datetime.utcnow(),
            )
        except (KeyError, IndexError, ValueError) as e:
            raise HTTPException(
                status_code=503, detail=f"Invalid weather API response: {str(e)}"
            ) from e

    def clear_cache_for_location(self, location: str) -> bool:
        """Clear weather cache for a specific location."""
        return self.weather_repository.clear_location_cache(location)

    def cleanup_expired_cache(self) -> int:
        """Clean up all expired weather cache entries."""
        return self.weather_repository.cleanup_expired_cache()

    def get_cached_locations(self) -> List[str]:
        """Get list of all currently cached locations."""
        return self.weather_repository.get_all_cached_locations()

    def has_cached_weather(self, location: str) -> bool:
        """Check if location has valid cached weather data."""
        return self.weather_repository.exists(location)
