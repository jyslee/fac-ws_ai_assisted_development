<!--
Trip Form Component - Handles both trip creation and editing
Follows established component patterns with TypeScript props, validation, and store integration
-->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { tripActions, tripStore } from '../stores/trips';
  import type { Trip, TripCreate, TripUpdate } from '../types/trip';

  // Props
  export let isEditing = false;
  export let trip: Trip | null = null;

  const dispatch = createEventDispatcher<{
    success: { trip: Trip };
    cancel: void;
  }>();

  // Form data
  const formData: TripCreate = {
    name: trip?.name || '',
    destination: trip?.destination || '',
    start_date: trip?.start_date || '',
    end_date: trip?.end_date || '',
    notes: trip?.notes || '',
  };

  // Validation state
  let errors: Record<string, string> = {};
  let isSubmitting = false;

  // Reactive store subscription
  $: ({ requestState } = $tripStore);
  $: isSubmitting = requestState.loading;

  // Date validation helper
  const validateDates = (): boolean => {
    const startDate = new Date(formData.start_date);
    const endDate = new Date(formData.end_date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (startDate < today) {
      errors.start_date = 'Start date cannot be in the past';
      return false;
    }

    if (endDate <= startDate) {
      errors.end_date = 'End date must be after start date';
      return false;
    }

    return true;
  };

  // Form validation
  const validateForm = (): boolean => {
    errors = {};

    // Required field validation
    if (!formData.name.trim()) {
      errors.name = 'Trip name is required';
    } else if (formData.name.length > 100) {
      errors.name = 'Trip name must be 100 characters or less';
    }

    if (!formData.destination.trim()) {
      errors.destination = 'Destination is required';
    }

    if (!formData.start_date) {
      errors.start_date = 'Start date is required';
    }

    if (!formData.end_date) {
      errors.end_date = 'End date is required';
    }

    // Notes validation
    if (formData.notes && formData.notes.length > 500) {
      errors.notes = 'Notes must be 500 characters or less';
    }

    // Date validation (only if both dates are provided)
    if (formData.start_date && formData.end_date) {
      validateDates();
    }

    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (): Promise<void> => {
    if (!validateForm()) {
      return;
    }

    let success = false;

    if (isEditing && trip) {
      // Update existing trip
      const updateData: TripUpdate = {
        name: formData.name,
        destination: formData.destination,
        start_date: formData.start_date,
        end_date: formData.end_date,
        notes: formData.notes || null,
      };
      success = await tripActions.updateTrip(trip.id, updateData);
    } else {
      // Create new trip
      const createData: TripCreate = {
        ...formData,
        notes: formData.notes || null,
      };
      success = await tripActions.createTrip(createData);
    }

    if (success) {
      // Find the updated/created trip and dispatch success event
      const trips = $tripStore.trips;
      const resultTrip = isEditing
        ? trips.find((t) => t.id === trip?.id)
        : trips[trips.length - 1]; // Last created trip

      if (resultTrip) {
        dispatch('success', { trip: resultTrip });
      }
    }
  };

  // Handle cancel
  const handleCancel = (): void => {
    dispatch('cancel');
  };

  // Clear field error on input
  const clearFieldError = (fieldName: string): void => {
    if (errors[fieldName]) {
      errors = { ...errors };
      delete errors[fieldName];
    }
  };
</script>

<div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
  <h2 class="text-xl font-semibold text-gray-900 mb-6">
    {isEditing ? 'Edit Trip' : 'Create New Trip'}
  </h2>

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <!-- Trip Name -->
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
        Trip Name *
      </label>
      <input
        id="name"
        type="text"
        bind:value={formData.name}
        on:input={() => clearFieldError('name')}
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        class:border-red-500={errors.name}
        placeholder="e.g., Paris Adventure"
        disabled={isSubmitting}
      />
      {#if errors.name}
        <p class="mt-1 text-sm text-red-600">{errors.name}</p>
      {/if}
    </div>

    <!-- Destination -->
    <div>
      <label
        for="destination"
        class="block text-sm font-medium text-gray-700 mb-1"
      >
        Destination *
      </label>
      <input
        id="destination"
        type="text"
        bind:value={formData.destination}
        on:input={() => clearFieldError('destination')}
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        class:border-red-500={errors.destination}
        placeholder="e.g., Paris, France"
        disabled={isSubmitting}
      />
      {#if errors.destination}
        <p class="mt-1 text-sm text-red-600">{errors.destination}</p>
      {/if}
    </div>

    <!-- Start Date -->
    <div>
      <label
        for="start_date"
        class="block text-sm font-medium text-gray-700 mb-1"
      >
        Start Date *
      </label>
      <input
        id="start_date"
        type="date"
        bind:value={formData.start_date}
        on:input={() => clearFieldError('start_date')}
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        class:border-red-500={errors.start_date}
        disabled={isSubmitting}
      />
      {#if errors.start_date}
        <p class="mt-1 text-sm text-red-600">{errors.start_date}</p>
      {/if}
    </div>

    <!-- End Date -->
    <div>
      <label
        for="end_date"
        class="block text-sm font-medium text-gray-700 mb-1"
      >
        End Date *
      </label>
      <input
        id="end_date"
        type="date"
        bind:value={formData.end_date}
        on:input={() => clearFieldError('end_date')}
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        class:border-red-500={errors.end_date}
        disabled={isSubmitting}
      />
      {#if errors.end_date}
        <p class="mt-1 text-sm text-red-600">{errors.end_date}</p>
      {/if}
    </div>

    <!-- Notes -->
    <div>
      <label for="notes" class="block text-sm font-medium text-gray-700 mb-1">
        Notes
      </label>
      <textarea
        id="notes"
        bind:value={formData.notes}
        on:input={() => clearFieldError('notes')}
        rows="3"
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        class:border-red-500={errors.notes}
        placeholder="Optional notes about your trip..."
        disabled={isSubmitting}
      />
      {#if errors.notes}
        <p class="mt-1 text-sm text-red-600">{errors.notes}</p>
      {/if}
    </div>

    <!-- Form Actions -->
    <div class="flex space-x-3 pt-4">
      <button
        type="submit"
        disabled={isSubmitting}
        class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed text-white py-2 px-4 rounded-md font-medium transition-colors duration-200 flex items-center justify-center"
      >
        {#if isSubmitting}
          <svg
            class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          {isEditing ? 'Updating...' : 'Creating...'}
        {:else}
          {isEditing ? 'Update Trip' : 'Create Trip'}
        {/if}
      </button>

      <button
        type="button"
        on:click={handleCancel}
        disabled={isSubmitting}
        class="flex-1 bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 disabled:cursor-not-allowed text-gray-700 py-2 px-4 rounded-md font-medium transition-colors duration-200"
      >
        Cancel
      </button>
    </div>
  </form>
</div>
