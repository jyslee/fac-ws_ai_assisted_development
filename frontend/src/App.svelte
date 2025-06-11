<script lang="ts">
  import { uiStore, showSuccessToast } from './stores/ui';
  import Toast from './lib/Toast.svelte';
  import WeatherWidgetSimple from './lib/WeatherWidgetSimple.svelte';
  
  const appName = 'Travel Planning App - Debug';
  
  let testMessage = 'Basic app loaded successfully!';
  
  const testToast = () => {
    showSuccessToast('Test toast notification!');
  };
</script>

<Toast />

<div class="min-h-screen bg-blue-100 p-8">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-gray-800 mb-4">{appName}</h1>
    <p class="text-lg text-gray-600 mb-8">{testMessage}</p>
    
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">Debug Info</h2>
      <p>If you can see this, the basic Svelte app is working.</p>
      <p>Next we'll add components one by one.</p>
      
      <button 
        on:click={testToast}
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Test Toast Store
      </button>
    </div>
    
    <div class="mt-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Weather Widget Test</h2>
      <div class="flex justify-center">
        <WeatherWidgetSimple />
      </div>
    </div>
  </div>
</div>