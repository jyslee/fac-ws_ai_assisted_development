<script lang="ts">
  import Toast from '$lib/Toast.svelte';
  import WeatherWidget from '$lib/WeatherWidget.svelte';
  import { uiStore } from '$stores/ui';
  import { onMount } from 'svelte';

  const appName = 'Travel Planning App';
  let mainWeatherLocation = '';

  const showSuccessDemo = () => {
    uiStore.showSuccess('Weather data loaded successfully!');
  };

  const showErrorDemo = () => {
    uiStore.showError('Failed to load weather data. Please try again.');
  };

  const showWarningDemo = () => {
    uiStore.showWarning('Weather data is from cache and may be outdated.');
  };

  const showInfoDemo = () => {
    uiStore.showInfo('Enter a location to check current weather conditions.');
  };

  onMount(() => {
    uiStore.showInfo('Welcome! Enter a location to check weather conditions.');
  });
</script>

<Toast />

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  <div class="container mx-auto px-4 py-8">
    <!-- Header Section -->
    <header class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">{appName}</h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">
        Plan your trips and check weather conditions for your destinations
      </p>
    </header>

    <!-- Main Weather Section -->
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Primary Weather Widget -->
        <div class="flex justify-center">
          <WeatherWidget
            bind:location={mainWeatherLocation}
            showLocationInput={true}
            autoFetch={false}
          />
        </div>

        <!-- Secondary Weather Widget (for demonstration) -->
        <div class="flex justify-center">
          <WeatherWidget
            location="Paris, France"
            showLocationInput={false}
            autoFetch={true}
          />
        </div>
      </div>

      <!-- Demo Controls Section -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">
          Toast Notifications Demo
        </h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <button
            on:click={showSuccessDemo}
            class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors duration-200 text-sm"
          >
            Success Toast
          </button>
          <button
            on:click={showErrorDemo}
            class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors duration-200 text-sm"
          >
            Error Toast
          </button>
          <button
            on:click={showWarningDemo}
            class="px-4 py-2 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 transition-colors duration-200 text-sm"
          >
            Warning Toast
          </button>
          <button
            on:click={showInfoDemo}
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors duration-200 text-sm"
          >
            Info Toast
          </button>
        </div>
      </div>

      <!-- Weather Features Section -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">
          Weather Features
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-3xl mb-2">🌡️</div>
            <h3 class="font-medium text-gray-800 mb-2">Real-time Data</h3>
            <p class="text-sm text-gray-600">
              Get current weather conditions including temperature, humidity,
              and wind speed
            </p>
          </div>
          <div class="text-center">
            <div class="text-3xl mb-2">⚡</div>
            <h3 class="font-medium text-gray-800 mb-2">Smart Caching</h3>
            <p class="text-sm text-gray-600">
              Weather data is cached for 30 minutes to improve performance and
              reduce API calls
            </p>
          </div>
          <div class="text-center">
            <div class="text-3xl mb-2">🌍</div>
            <h3 class="font-medium text-gray-800 mb-2">Global Locations</h3>
            <p class="text-sm text-gray-600">
              Check weather for any location worldwide by entering city names or
              coordinates
            </p>
          </div>
        </div>
      </div>

      <!-- Instructions Section -->
      <div class="mt-8 text-center">
        <p class="text-gray-600 mb-2">
          Enter a location in the weather widget above to get started
        </p>
        <p class="text-sm text-gray-500">
          Try locations like "London", "New York", "Tokyo", or "Sydney"
        </p>
      </div>
    </div>
  </div>
</div>
