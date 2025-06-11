<script lang="ts">
  import { weatherStore, weatherActions } from '../stores/weather';
  import type { WeatherData } from '../types/weather';

  export let location: string = '';
  
  let inputLocation = location;
  let weatherData: WeatherData | null = null;
  let isLoading = false;
  let errorMessage = '';

  const fetchWeather = async () => {
    if (!inputLocation.trim()) {
      return;
    }
    
    isLoading = true;
    errorMessage = '';
    
    try {
      const result = await weatherActions.getWeatherByLocation(inputLocation.trim());
      weatherData = result;
      if (!result) {
        errorMessage = 'No weather data available';
      }
    } catch (error) {
      errorMessage = 'Failed to fetch weather data';
    } finally {
      isLoading = false;
    }
  };

  const handleSubmit = () => {
    if (inputLocation.trim()) {
      location = inputLocation.trim();
      fetchWeather();
    }
  };

  const handleKeyPress = (event: KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  };

  const formatTemperature = (temp: number): string => {
    return `${Math.round(temp)}°C`;
  };

  const getWeatherIcon = (condition: string): string => {
    const lowercaseCondition = condition.toLowerCase();
    
    if (lowercaseCondition.includes('clear') || lowercaseCondition.includes('sunny')) {
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
</script>

<div class="bg-white rounded-lg shadow-md p-4 max-w-sm w-full">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-gray-800">Weather</h3>
  </div>

  <div class="mb-4">
    <div class="flex space-x-2">
      <input
        type="text"
        bind:value={inputLocation}
        on:keypress={handleKeyPress}
        placeholder="Enter location..."
        class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        disabled={isLoading}
      />
      <button
        on:click={handleSubmit}
        disabled={isLoading || !inputLocation.trim()}
        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
      >
        {#if isLoading}
          <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        {:else}
          Get Weather
        {/if}
      </button>
    </div>
  </div>

  <div class="weather-content">
    {#if isLoading}
      <div class="flex items-center justify-center py-8">
        <div class="flex items-center space-x-2">
          <div class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-600">Loading weather...</span>
        </div>
      </div>
    {:else if errorMessage}
      <div class="text-center py-8">
        <div class="text-red-500 mb-2">
          <span class="text-2xl">⚠️</span>
        </div>
        <p class="text-red-600 text-sm font-medium mb-2">Weather Unavailable</p>
        <p class="text-gray-600 text-xs">{errorMessage}</p>
        <button
          on:click={fetchWeather}
          class="mt-3 px-3 py-1 text-xs bg-red-100 text-red-600 rounded hover:bg-red-200 transition-colors duration-200"
        >
          Try Again
        </button>
      </div>
    {:else if weatherData}
      <div class="space-y-4">
        <div class="text-center">
          <div class="text-3xl mb-2">{getWeatherIcon(weatherData.condition)}</div>
          <h4 class="font-medium text-gray-800 mb-1">{weatherData.location}</h4>
          <p class="text-2xl font-bold text-blue-600">{formatTemperature(weatherData.temperature)}</p>
          <p class="text-sm text-gray-600 capitalize">{weatherData.condition}</p>
        </div>
        
        <div class="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
          <div class="text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wide">Humidity</p>
            <p class="text-lg font-semibold text-gray-800">{weatherData.humidity}%</p>
          </div>
          <div class="text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wide">Wind</p>
            <p class="text-lg font-semibold text-gray-800">{weatherData.wind_speed} km/h</p>
          </div>
        </div>
        
        {#if weatherData.updated_at}
          <div class="text-center pt-2">
            <p class="text-xs text-gray-400">
              Updated: {new Date(weatherData.updated_at).toLocaleTimeString()}
            </p>
          </div>
        {/if}
      </div>
    {:else}
      <div class="text-center py-8">
        <div class="text-gray-400 mb-2">
          <span class="text-2xl">📍</span>
        </div>
        <p class="text-gray-600 text-sm">Enter a location to see weather</p>
      </div>
    {/if}
  </div>
</div>