import type { Trip, TripCreate, TripUpdate } from '../types/trip';
import type { APIResult } from './api';
import { apiClient } from './api';

/**
 * Trip service layer providing typed CRUD operations for trip management
 * Abstracts API communication and provides consistent error handling
 */
export class TripService {
  private readonly baseEndpoint = '/api/trips';

  /**
   * Get all trips from the backend
   */
  async getAllTrips(): Promise<APIResult<Trip[]>> {
    return apiClient.get<Trip[]>(this.baseEndpoint);
  }

  /**
   * Get a specific trip by ID
   */
  async getTripById(id: number): Promise<APIResult<Trip>> {
    return apiClient.get<Trip>(`${this.baseEndpoint}/${id}`);
  }

  /**
   * Create a new trip
   */
  async createTrip(tripData: TripCreate): Promise<APIResult<Trip>> {
    return apiClient.post<Trip>(this.baseEndpoint, tripData);
  }

  /**
   * Update an existing trip
   */
  async updateTrip(id: number, tripData: TripUpdate): Promise<APIResult<Trip>> {
    return apiClient.put<Trip>(`${this.baseEndpoint}/${id}`, tripData);
  }

  /**
   * Delete a trip by ID
   */
  async deleteTrip(id: number): Promise<APIResult<void>> {
    return apiClient.delete<void>(`${this.baseEndpoint}/${id}`);
  }
}

// Export singleton instance for use throughout the application
export const tripService = new TripService();
