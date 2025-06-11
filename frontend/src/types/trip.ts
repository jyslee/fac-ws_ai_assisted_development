/**
 * Trip-related TypeScript type definitions matching backend models
 */

export interface Trip {
  id: number;
  name: string;
  destination: string;
  start_date: string; // ISO date string (YYYY-MM-DD)
  end_date: string; // ISO date string (YYYY-MM-DD)
  notes: string | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  duration_days: number;
}

export interface TripCreate {
  name: string;
  destination: string;
  start_date: string; // ISO date string (YYYY-MM-DD)
  end_date: string; // ISO date string (YYYY-MM-DD)
  notes?: string | null;
}

export interface TripUpdate {
  name?: string;
  destination?: string;
  start_date?: string; // ISO date string (YYYY-MM-DD)
  end_date?: string; // ISO date string (YYYY-MM-DD)
  notes?: string | null;
}

export type TripFormData = TripCreate;
export type TripEditData = TripUpdate;
