<!--
Main Application Component - Complete Travel Planning App
Integrates trip management, weather display, and modal handling
-->
<script lang="ts">
  import { onMount } from 'svelte';
  import { tripStore, tripActions } from './stores/trips';
  import './stores/ui';
  import Toast from './lib/Toast.svelte';
  import TripCard from './lib/TripCard.svelte';
  import TripForm from './lib/TripForm.svelte';
  import WeatherWidgetSimple from './lib/WeatherWidgetSimple.svelte';
  import type { Trip } from './types/trip';

  // Modal state
  let showTripForm = false;
  let editingTrip: Trip | null = null;
  let showDeleteConfirm = false;
  let tripToDelete: Trip | null = null;

  // Reactive store subscriptions
  $: ({ trips, requestState } = $tripStore);
  $: isLoading = requestState.loading;

  // Load trips on component mount
  onMount(() => {
    tripActions.loadTrips();
  });

  // Modal handlers
  const openCreateModal = (): void => {
    editingTrip = null;
    showTripForm = true;
  };

  const openEditModal = (trip: Trip): void => {
    editingTrip = trip;
    showTripForm = true;
  };

  const closeModal = (): void => {
    showTripForm = false;
    editingTrip = null;
  };

  const openDeleteConfirm = (trip: Trip): void => {
    tripToDelete = trip;
    showDeleteConfirm = true;
  };

  const closeDeleteConfirm = (): void => {
    showDeleteConfirm = false;
    tripToDelete = null;
  };

  // Trip handlers
  const handleTripFormSuccess = (): void => {
    closeModal();
  };

  const handleEditTrip = (event: CustomEvent<{ trip: Trip }>): void => {
    openEditModal(event.detail.trip);
  };

  const handleDeleteTrip = (event: CustomEvent<{ trip: Trip }>): void => {
    openDeleteConfirm(event.detail.trip);
  };

  const confirmDelete = async (): Promise<void> => {
    if (tripToDelete) {
      const success = await tripActions.deleteTrip(tripToDelete.id);
      if (success) {
        closeDeleteConfirm();
      }
    }
  };

  // Sort trips by start date (upcoming first)
  $: sortedTrips = trips.slice().sort((a, b) => {
    return new Date(a.start_date).getTime() - new Date(b.start_date).getTime();
  });

  // Trip status helpers
  const getTripStatus = (
    startDate: string,
    endDate: string
  ): 'upcoming' | 'current' | 'past' => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const start = new Date(startDate);
    const end = new Date(endDate);

    if (start > today) return 'upcoming';
    if (end >= today) return 'current';
    return 'past';
  };

  $: upcomingTrips = sortedTrips.filter(
    (trip) => getTripStatus(trip.start_date, trip.end_date) === 'upcoming'
  );
  $: currentTrips = sortedTrips.filter(
    (trip) => getTripStatus(trip.start_date, trip.end_date) === 'current'
  );
  $: pastTrips = sortedTrips.filter(
    (trip) => getTripStatus(trip.start_date, trip.end_date) === 'past'
  );
</script>

<!-- Toast notifications -->
<Toast />

<!-- Main App Container -->
<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  <!-- Header -->
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">
            Travel Planning App
          </h1>
          <p class="text-gray-600 text-sm sm:text-base">
            Plan your trips and check the weather
          </p>
        </div>
        <button
          on:click={openCreateModal}
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
        >
          <span>✈️</span>
          <span class="hidden sm:inline">New Trip</span>
          <span class="sm:hidden">+</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Weather Widget Section -->
    <section class="mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Weather Check</h2>
      <div class="flex justify-center">
        <WeatherWidgetSimple />
      </div>
    </section>

    <!-- Trips Section -->
    <section>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">Your Trips</h2>
        {#if trips.length > 0}
          <span class="text-sm text-gray-500"
            >{trips.length} {trips.length === 1 ? 'trip' : 'trips'}</span
          >
        {/if}
      </div>

      <!-- Loading State -->
      {#if isLoading && trips.length === 0}
        <div class="flex items-center justify-center py-12">
          <div class="flex items-center space-x-3">
            <div
              class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"
            />
            <span class="text-gray-600">Loading your trips...</span>
          </div>
        </div>

        <!-- Empty State -->
      {:else if trips.length === 0}
        <div class="text-center py-12">
          <div class="text-6xl mb-4">✈️</div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No trips yet</h3>
          <p class="text-gray-600 mb-6">Start planning your next adventure!</p>
          <button
            on:click={openCreateModal}
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            Create Your First Trip
          </button>
        </div>

        <!-- Trips Display -->
      {:else}
        <!-- Current Trips -->
        {#if currentTrips.length > 0}
          <div class="mb-8">
            <h3
              class="text-lg font-medium text-green-700 mb-4 flex items-center"
            >
              <span class="mr-2">🌟</span>
              Current Trip{currentTrips.length > 1 ? 's' : ''} ({currentTrips.length})
            </h3>
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {#each currentTrips as trip (trip.id)}
                <TripCard
                  {trip}
                  on:edit={handleEditTrip}
                  on:delete={handleDeleteTrip}
                />
              {/each}
            </div>
          </div>
        {/if}

        <!-- Upcoming Trips -->
        {#if upcomingTrips.length > 0}
          <div class="mb-8">
            <h3
              class="text-lg font-medium text-blue-700 mb-4 flex items-center"
            >
              <span class="mr-2">📅</span>
              Upcoming Trip{upcomingTrips.length > 1 ? 's' : ''} ({upcomingTrips.length})
            </h3>
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {#each upcomingTrips as trip (trip.id)}
                <TripCard
                  {trip}
                  on:edit={handleEditTrip}
                  on:delete={handleDeleteTrip}
                />
              {/each}
            </div>
          </div>
        {/if}

        <!-- Past Trips -->
        {#if pastTrips.length > 0}
          <div>
            <h3
              class="text-lg font-medium text-gray-600 mb-4 flex items-center"
            >
              <span class="mr-2">📖</span>
              Past Trip{pastTrips.length > 1 ? 's' : ''} ({pastTrips.length})
            </h3>
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {#each pastTrips as trip (trip.id)}
                <TripCard
                  {trip}
                  on:edit={handleEditTrip}
                  on:delete={handleDeleteTrip}
                />
              {/each}
            </div>
          </div>
        {/if}
      {/if}
    </section>
  </main>
</div>

<!-- Trip Form Modal -->
{#if showTripForm}
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
  >
    <div
      class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto"
    >
      <TripForm
        isEditing={!!editingTrip}
        trip={editingTrip}
        on:success={handleTripFormSuccess}
        on:cancel={closeModal}
      />
    </div>
  </div>
{/if}

<!-- Delete Confirmation Modal -->
{#if showDeleteConfirm && tripToDelete}
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
  >
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Delete Trip</h3>
      <p class="text-gray-600 mb-6">
        Are you sure you want to delete <strong>"{tripToDelete.name}"</strong>?
        This action cannot be undone.
      </p>
      <div class="flex space-x-3">
        <button
          on:click={confirmDelete}
          disabled={isLoading}
          class="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white py-2 px-4 rounded-md font-medium transition-colors duration-200"
        >
          {isLoading ? 'Deleting...' : 'Delete Trip'}
        </button>
        <button
          on:click={closeDeleteConfirm}
          disabled={isLoading}
          class="flex-1 bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 text-gray-700 py-2 px-4 rounded-md font-medium transition-colors duration-200"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
{/if}
