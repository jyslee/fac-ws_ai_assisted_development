import type { WeatherData } from '../types/weather';
import type { APIResult } from './api';
import { apiClient } from './api';

/**
 * Weather service layer providing typed operations for weather data fetching
 * Abstracts API communication and provides consistent error handling for weather operations
 */
export class WeatherService {
  private readonly baseEndpoint = '/api/weather';

  /**
   * Get weather data for a specific location
   * @param location The location to get weather for (e.g., "Paris, France")
   */
  async getWeatherByLocation(
    location: string
  ): Promise<APIResult<WeatherData>> {
    // Encode the location to handle spaces and special characters in URLs
    const encodedLocation = encodeURIComponent(location);
    return apiClient.get<WeatherData>(
      `${this.baseEndpoint}/${encodedLocation}`
    );
  }

  /**
   * Get weather data for a trip's destination
   * @param tripId The ID of the trip to get weather for
   */
  async getWeatherForTrip(tripId: number): Promise<APIResult<WeatherData>> {
    return apiClient.get<WeatherData>(`/api/trips/${tripId}/weather`);
  }
}

// Export singleton instance for use throughout the application
export const weatherService = new WeatherService();
