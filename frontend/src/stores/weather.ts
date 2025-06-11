/**
 * Weather Store for state management of location-based weather data
 */

import { get, writable } from 'svelte/store';
import { weatherService } from '../services/weatherService';
import type { WeatherCache, WeatherData, WeatherState } from '../types/weather';
import { showErrorToast } from './ui';

interface WeatherStoreState {
  cache: WeatherCache;
  globalLoading: boolean;
}

const initialState: WeatherStoreState = {
  cache: {},
  globalLoading: false,
};

export const weatherStore = writable<WeatherStoreState>(initialState);

const CACHE_DURATION_MS = 30 * 60 * 1000; // 30 minutes

export const weatherActions = {
  /**
   * Get weather data for a specific location
   * Uses cache if data is fresh, otherwise fetches from API
   */
  getWeatherByLocation: async (
    location: string
  ): Promise<WeatherData | null> => {
    const normalizedLocation = location.trim();

    if (!normalizedLocation) {
      showErrorToast('Please provide a valid location');
      return null;
    }

    // Check if we have cached data and if it's still fresh
    const currentState = get(weatherStore);
    const cachedState = currentState.cache[normalizedLocation];

    if (cachedState?.data && !cachedState.loading && !cachedState.error) {
      const cacheAge =
        Date.now() - new Date(cachedState.data.updated_at).getTime();
      if (cacheAge < CACHE_DURATION_MS) {
        return cachedState.data;
      }
    }

    // Set loading state for this location
    weatherStore.update((state) => ({
      ...state,
      cache: {
        ...state.cache,
        [normalizedLocation]: {
          data: cachedState?.data || null,
          loading: true,
          error: null,
        },
      },
    }));

    try {
      const result = await weatherService.getWeatherByLocation(
        normalizedLocation
      );

      if (result.success && result.data) {
        weatherStore.update((state) => ({
          ...state,
          cache: {
            ...state.cache,
            [normalizedLocation]: {
              data: result.data!,
              loading: false,
              error: null,
            },
          },
        }));
        return result.data;
      } else {
        const errorMessage =
          result.error?.message || 'Failed to fetch weather data';
        weatherStore.update((state) => ({
          ...state,
          cache: {
            ...state.cache,
            [normalizedLocation]: {
              data: cachedState?.data || null,
              loading: false,
              error: errorMessage,
            },
          },
        }));
        showErrorToast(`Weather: ${errorMessage}`);
        return null;
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      weatherStore.update((state) => ({
        ...state,
        cache: {
          ...state.cache,
          [normalizedLocation]: {
            data: cachedState?.data || null,
            loading: false,
            error: errorMessage,
          },
        },
      }));
      showErrorToast(`Weather error: ${errorMessage}`);
      return null;
    }
  },

  /**
   * Get weather data for a trip's destination
   */
  getWeatherForTrip: async (
    tripId: number,
    destination: string
  ): Promise<WeatherData | null> => {
    const normalizedLocation = destination.trim();

    if (!normalizedLocation) {
      showErrorToast('Trip destination is not specified');
      return null;
    }

    // Check cache first
    const currentState = get(weatherStore);
    const cachedState = currentState.cache[normalizedLocation];

    if (cachedState?.data && !cachedState.loading && !cachedState.error) {
      const cacheAge =
        Date.now() - new Date(cachedState.data.updated_at).getTime();
      if (cacheAge < CACHE_DURATION_MS) {
        return cachedState.data;
      }
    }

    // Set loading state
    weatherStore.update((state) => ({
      ...state,
      cache: {
        ...state.cache,
        [normalizedLocation]: {
          data: cachedState?.data || null,
          loading: true,
          error: null,
        },
      },
    }));

    try {
      const result = await weatherService.getWeatherForTrip(tripId);

      if (result.success && result.data) {
        weatherStore.update((state) => ({
          ...state,
          cache: {
            ...state.cache,
            [normalizedLocation]: {
              data: result.data!,
              loading: false,
              error: null,
            },
          },
        }));
        return result.data;
      } else {
        const errorMessage =
          result.error?.message || 'Failed to fetch trip weather data';
        weatherStore.update((state) => ({
          ...state,
          cache: {
            ...state.cache,
            [normalizedLocation]: {
              data: cachedState?.data || null,
              loading: false,
              error: errorMessage,
            },
          },
        }));
        showErrorToast(`Trip weather: ${errorMessage}`);
        return null;
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      weatherStore.update((state) => ({
        ...state,
        cache: {
          ...state.cache,
          [normalizedLocation]: {
            data: cachedState?.data || null,
            loading: false,
            error: errorMessage,
          },
        },
      }));
      showErrorToast(`Trip weather error: ${errorMessage}`);
      return null;
    }
  },

  /**
   * Get weather state for a specific location from cache
   */
  getWeatherState: (location: string): WeatherState => {
    const currentState = get(weatherStore);
    return (
      currentState.cache[location.trim()] || {
        data: null,
        loading: false,
        error: null,
      }
    );
  },

  /**
   * Clear weather data for a specific location
   */
  clearWeatherForLocation: (location: string): void => {
    weatherStore.update((state) => {
      const newCache = { ...state.cache };
      delete newCache[location.trim()];
      return {
        ...state,
        cache: newCache,
      };
    });
  },

  /**
   * Clear all cached weather data
   */
  clearAllWeatherCache: (): void => {
    weatherStore.update((state) => ({
      ...state,
      cache: {},
    }));
  },

  /**
   * Clear error for a specific location
   */
  clearErrorForLocation: (location: string): void => {
    weatherStore.update((state) => {
      const locationData = state.cache[location.trim()];
      if (locationData) {
        return {
          ...state,
          cache: {
            ...state.cache,
            [location.trim()]: {
              ...locationData,
              error: null,
            },
          },
        };
      }
      return state;
    });
  },
};
