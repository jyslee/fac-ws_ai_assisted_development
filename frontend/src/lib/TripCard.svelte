<!--
Trip Card Component - Displays trip information with integrated weather display
Follows established component patterns with TypeScript props, weather integration, and responsive design
-->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { weatherActions } from '../stores/weather';
  import type { Trip } from '../types/trip';
  import type { WeatherData } from '../types/weather';

  // Props
  export let trip: Trip;

  const dispatch = createEventDispatcher<{
    edit: { trip: Trip };
    delete: { trip: Trip };
  }>();

  // Weather state
  let weatherData: WeatherData | null = null;
  let isLoadingWeather = false;
  let weatherError = '';

  // Calculate trip duration for display
  const formatDuration = (days: number): string => {
    if (days === 1) return '1 day';
    return `${days} days`;
  };

  // Format dates for display
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  // Check if trip is in the future, current, or past
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

  // Get status styling
  const getStatusStyle = (status: string): string => {
    switch (status) {
      case 'upcoming':
        return 'bg-blue-100 text-blue-800';
      case 'current':
        return 'bg-green-100 text-green-800';
      case 'past':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Weather integration
  const loadWeather = async (): Promise<void> => {
    if (!trip.destination) return;

    isLoadingWeather = true;
    weatherError = '';

    try {
      const result = await weatherActions.getWeatherByLocation(
        trip.destination
      );
      weatherData = result;
      if (!result) {
        weatherError = 'Weather unavailable';
      }
    } catch (error) {
      weatherError = 'Failed to load weather';
    } finally {
      isLoadingWeather = false;
    }
  };

  // Weather icon helper
  const getWeatherIcon = (condition: string): string => {
    const lowercaseCondition = condition.toLowerCase();

    if (
      lowercaseCondition.includes('clear') ||
      lowercaseCondition.includes('sunny')
    ) {
      return '☀️';
    } else if (lowercaseCondition.includes('cloud')) {
      return '☁️';
    } else if (lowercaseCondition.includes('rain')) {
      return '🌧️';
    } else if (lowercaseCondition.includes('snow')) {
      return '❄️';
    } else {
      return '🌤️';
    }
  };

  // Temperature formatting
  const formatTemperature = (temp: number): string => {
    return `${Math.round(temp)}°C`;
  };

  // Event handlers
  const handleEdit = (): void => {
    dispatch('edit', { trip });
  };

  const handleDelete = (): void => {
    dispatch('delete', { trip });
  };

  // Load weather on component mount
  import { onMount } from 'svelte';
  onMount(() => {
    loadWeather();
  });

  // Reactive status calculation
  $: tripStatus = getTripStatus(trip.start_date, trip.end_date);
  $: statusLabel = tripStatus.charAt(0).toUpperCase() + tripStatus.slice(1);
</script>

<div
  class="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-200"
>
  <!-- Trip Header -->
  <div class="p-4 pb-2">
    <div class="flex items-start justify-between mb-2">
      <h3 class="text-lg font-semibold text-gray-900 flex-1 mr-4">
        {trip.name}
      </h3>
      <span
        class="px-2 py-1 text-xs font-medium rounded-full {getStatusStyle(
          tripStatus
        )}"
      >
        {statusLabel}
      </span>
    </div>

    <div class="space-y-2">
      <!-- Destination -->
      <div class="flex items-center text-gray-600">
        <span class="mr-2">📍</span>
        <span class="text-sm font-medium">{trip.destination}</span>
      </div>

      <!-- Dates -->
      <div class="flex items-center text-gray-600">
        <span class="mr-2">📅</span>
        <span class="text-sm">
          {formatDate(trip.start_date)} - {formatDate(trip.end_date)}
          <span class="text-gray-400 ml-1"
            >({formatDuration(trip.duration_days)})</span
          >
        </span>
      </div>

      <!-- Notes (if any) -->
      {#if trip.notes}
        <div class="flex items-start text-gray-600">
          <span class="mr-2 mt-0.5">📝</span>
          <span class="text-sm">{trip.notes}</span>
        </div>
      {/if}
    </div>
  </div>

  <!-- Weather Section -->
  <div class="px-4 pb-2">
    <div class="bg-gray-50 rounded-md p-3 border border-gray-100">
      <div class="flex items-center justify-between mb-2">
        <h4 class="text-sm font-medium text-gray-700">Weather</h4>
        {#if !isLoadingWeather && !weatherError}
          <button
            on:click={loadWeather}
            class="text-xs text-blue-600 hover:text-blue-800 transition-colors duration-200"
            title="Refresh weather"
          >
            🔄
          </button>
        {/if}
      </div>

      {#if isLoadingWeather}
        <div class="flex items-center justify-center py-2">
          <div class="flex items-center space-x-2 text-gray-500">
            <div
              class="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"
            />
            <span class="text-xs">Loading...</span>
          </div>
        </div>
      {:else if weatherError}
        <div class="text-center py-2">
          <span class="text-xs text-red-600">{weatherError}</span>
          <button
            on:click={loadWeather}
            class="ml-2 text-xs text-red-600 hover:text-red-800 underline"
          >
            Retry
          </button>
        </div>
      {:else if weatherData}
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-lg">{getWeatherIcon(weatherData.condition)}</span>
            <div>
              <p class="text-sm font-medium text-gray-800">
                {formatTemperature(weatherData.temperature)}
              </p>
              <p class="text-xs text-gray-600 capitalize">
                {weatherData.condition}
              </p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">💧 {weatherData.humidity}%</p>
            <p class="text-xs text-gray-500">
              💨 {weatherData.wind_speed} km/h
            </p>
          </div>
        </div>
      {:else}
        <div class="text-center py-2">
          <span class="text-xs text-gray-500">Weather data unavailable</span>
        </div>
      {/if}
    </div>
  </div>

  <!-- Actions -->
  <div class="px-4 pb-4">
    <div class="flex space-x-2">
      <button
        on:click={handleEdit}
        class="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 py-2 px-3 rounded-md text-sm font-medium transition-colors duration-200 flex items-center justify-center"
      >
        <span class="mr-1">✏️</span>
        Edit
      </button>
      <button
        on:click={handleDelete}
        class="flex-1 bg-red-50 hover:bg-red-100 text-red-700 py-2 px-3 rounded-md text-sm font-medium transition-colors duration-200 flex items-center justify-center"
      >
        <span class="mr-1">🗑️</span>
        Delete
      </button>
    </div>
  </div>

  <!-- Trip Created Date (Footer) -->
  <div class="px-4 py-2 bg-gray-50 border-t border-gray-100">
    <p class="text-xs text-gray-400">
      Created: {new Date(trip.created_at).toLocaleDateString()}
    </p>
  </div>
</div>
