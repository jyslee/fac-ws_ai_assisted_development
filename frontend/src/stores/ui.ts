/**
 * UI Store for toast notifications and general UI state management
 */

import { writable } from 'svelte/store';
import type { Toast, ToastState } from '../types/api';

const initialState: ToastState = {
  toasts: [],
};

export const uiStore = writable<ToastState>(initialState);

let toastIdCounter = 0;

export const uiActions = {
  showToast: (type: Toast['type'], message: string, duration = 5000): void => {
    const toast: Toast = {
      id: `toast-${++toastIdCounter}`,
      type,
      message,
      duration,
    };

    uiStore.update((state) => ({
      ...state,
      toasts: [...state.toasts, toast],
    }));

    if (duration > 0) {
      setTimeout(() => {
        uiActions.hideToast(toast.id);
      }, duration);
    }
  },

  hideToast: (toastId: string): void => {
    uiStore.update((state) => ({
      ...state,
      toasts: state.toasts.filter((toast) => toast.id !== toastId),
    }));
  },

  clearAllToasts: (): void => {
    uiStore.update((state) => ({
      ...state,
      toasts: [],
    }));
  },
};

export const showSuccessToast = (message: string, duration?: number): void => {
  uiActions.showToast('success', message, duration);
};

export const showErrorToast = (message: string, duration?: number): void => {
  uiActions.showToast('error', message, duration);
};

export const showWarningToast = (message: string, duration?: number): void => {
  uiActions.showToast('warning', message, duration);
};

export const showInfoToast = (message: string, duration?: number): void => {
  uiActions.showToast('info', message, duration);
};
