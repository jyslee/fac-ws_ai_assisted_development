/**
 * Weather-related TypeScript type definitions matching backend models
 */

export interface WeatherData {
  location: string;
  temperature: number; // Temperature in Celsius
  condition: string;
  humidity: number; // Percentage (0-100)
  wind_speed: number; // Wind speed in km/h
  updated_at: string; // ISO datetime string
}

export interface WeatherState {
  data: WeatherData | null;
  loading: boolean;
  error: string | null;
}

export interface WeatherCache {
  [location: string]: WeatherState;
}
