/**
 * Trip Store for state management of all trip-related data and operations
 */

import { writable } from 'svelte/store';
import { tripService } from '../services/tripService';
import type { RequestState } from '../types/api';
import type { Trip, TripCreate, TripUpdate } from '../types/trip';
import { showErrorToast, showSuccessToast } from './ui';

interface TripState {
  trips: Trip[];
  selectedTrip: Trip | null;
  requestState: RequestState;
}

const initialState: TripState = {
  trips: [],
  selectedTrip: null,
  requestState: {
    loading: false,
    error: null,
  },
};

export const tripStore = writable<TripState>(initialState);

export const tripActions = {
  /**
   * Load all trips from the backend
   */
  loadTrips: async (): Promise<void> => {
    tripStore.update((state) => ({
      ...state,
      requestState: { loading: true, error: null },
    }));

    try {
      const result = await tripService.getAllTrips();

      if (result.success && result.data) {
        tripStore.update((state) => ({
          ...state,
          trips: result.data!,
          requestState: { loading: false, error: null },
        }));
      } else {
        const errorMessage = result.error?.message || 'Failed to load trips';
        tripStore.update((state) => ({
          ...state,
          requestState: { loading: false, error: errorMessage },
        }));
        showErrorToast(`Failed to load trips: ${errorMessage}`);
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      tripStore.update((state) => ({
        ...state,
        requestState: { loading: false, error: errorMessage },
      }));
      showErrorToast(`Failed to load trips: ${errorMessage}`);
    }
  },

  /**
   * Create a new trip
   */
  createTrip: async (tripData: TripCreate): Promise<boolean> => {
    tripStore.update((state) => ({
      ...state,
      requestState: { loading: true, error: null },
    }));

    try {
      const result = await tripService.createTrip(tripData);

      if (result.success && result.data) {
        tripStore.update((state) => ({
          ...state,
          trips: [...state.trips, result.data!],
          requestState: { loading: false, error: null },
        }));
        showSuccessToast(`Trip "${result.data!.name}" created successfully`);
        return true;
      } else {
        const errorMessage = result.error?.message || 'Failed to create trip';
        tripStore.update((state) => ({
          ...state,
          requestState: { loading: false, error: errorMessage },
        }));
        showErrorToast(`Failed to create trip: ${errorMessage}`);
        return false;
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      tripStore.update((state) => ({
        ...state,
        requestState: { loading: false, error: errorMessage },
      }));
      showErrorToast(`Failed to create trip: ${errorMessage}`);
      return false;
    }
  },

  /**
   * Update an existing trip
   */
  updateTrip: async (
    tripId: number,
    tripData: TripUpdate
  ): Promise<boolean> => {
    tripStore.update((state) => ({
      ...state,
      requestState: { loading: true, error: null },
    }));

    try {
      const result = await tripService.updateTrip(tripId, tripData);

      if (result.success && result.data) {
        tripStore.update((state) => ({
          ...state,
          trips: state.trips.map((trip) =>
            trip.id === tripId ? result.data! : trip
          ),
          selectedTrip:
            state.selectedTrip?.id === tripId
              ? result.data!
              : state.selectedTrip,
          requestState: { loading: false, error: null },
        }));
        showSuccessToast(`Trip "${result.data!.name}" updated successfully`);
        return true;
      } else {
        const errorMessage = result.error?.message || 'Failed to update trip';
        tripStore.update((state) => ({
          ...state,
          requestState: { loading: false, error: errorMessage },
        }));
        showErrorToast(`Failed to update trip: ${errorMessage}`);
        return false;
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      tripStore.update((state) => ({
        ...state,
        requestState: { loading: false, error: errorMessage },
      }));
      showErrorToast(`Failed to update trip: ${errorMessage}`);
      return false;
    }
  },

  /**
   * Delete a trip
   */
  deleteTrip: async (tripId: number): Promise<boolean> => {
    let tripName = '';

    // Get trip name for success message
    tripStore.update((state) => {
      const trip = state.trips.find((t) => t.id === tripId);
      tripName = trip?.name || 'Trip';
      return {
        ...state,
        requestState: { loading: true, error: null },
      };
    });

    try {
      const result = await tripService.deleteTrip(tripId);

      if (result.success) {
        tripStore.update((state) => ({
          ...state,
          trips: state.trips.filter((trip) => trip.id !== tripId),
          selectedTrip:
            state.selectedTrip?.id === tripId ? null : state.selectedTrip,
          requestState: { loading: false, error: null },
        }));
        showSuccessToast(`Trip "${tripName}" deleted successfully`);
        return true;
      } else {
        const errorMessage = result.error?.message || 'Failed to delete trip';
        tripStore.update((state) => ({
          ...state,
          requestState: { loading: false, error: errorMessage },
        }));
        showErrorToast(`Failed to delete trip: ${errorMessage}`);
        return false;
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      tripStore.update((state) => ({
        ...state,
        requestState: { loading: false, error: errorMessage },
      }));
      showErrorToast(`Failed to delete trip: ${errorMessage}`);
      return false;
    }
  },

  /**
   * Select a trip for detailed view
   */
  selectTrip: (trip: Trip | null): void => {
    tripStore.update((state) => ({
      ...state,
      selectedTrip: trip,
    }));
  },

  /**
   * Clear any existing errors
   */
  clearError: (): void => {
    tripStore.update((state) => ({
      ...state,
      requestState: { ...state.requestState, error: null },
    }));
  },
};
