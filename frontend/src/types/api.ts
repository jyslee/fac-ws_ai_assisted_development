/**
 * API-related TypeScript type definitions for HTTP communication
 */

export interface APIResponse<T> {
  data: T;
  message?: string;
}

export interface APIError {
  message: string;
  detail?: string;
  status: number;
}

export interface RequestState {
  loading: boolean;
  error: string | null;
}

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number; // Duration in milliseconds
}

export interface ToastState {
  toasts: Toast[];
}

export type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

export interface APIClientConfig {
  baseURL: string;
  timeout?: number;
}

export interface APIRequestOptions {
  method: HTTPMethod;
  body?: unknown;
  headers?: Record<string, string>;
}
