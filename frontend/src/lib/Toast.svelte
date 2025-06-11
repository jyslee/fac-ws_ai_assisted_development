<script lang="ts">
  import { onMount } from 'svelte';
  import { uiStore } from '../stores/ui';
  import type { Toast } from '../types/api';

  let toasts: Toast[] = [];

  const removeToast = (id: string) => {
    uiStore.hideToast(id);
  };

  const getToastIcon = (type: string): string => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      case 'info':
      default:
        return 'ℹ';
    }
  };

  const getToastClasses = (type: string): string => {
    const baseClasses =
      'flex items-center p-4 mb-2 rounded-lg shadow-lg transition-all duration-300 ease-in-out transform';

    switch (type) {
      case 'success':
        return `${baseClasses} bg-green-100 border-l-4 border-green-500 text-green-700`;
      case 'error':
        return `${baseClasses} bg-red-100 border-l-4 border-red-500 text-red-700`;
      case 'warning':
        return `${baseClasses} bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700`;
      case 'info':
      default:
        return `${baseClasses} bg-blue-100 border-l-4 border-blue-500 text-blue-700`;
    }
  };

  onMount(() => {
    const unsubscribe = uiStore.subscribe((state) => {
      toasts = state.toasts;
    });

    return unsubscribe;
  });
</script>

<div class="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
  {#each toasts as toast (toast.id)}
    <div class={getToastClasses(toast.type)} role="alert" aria-live="polite">
      <div class="flex-shrink-0 mr-3">
        <span class="text-lg font-bold" aria-hidden="true">
          {getToastIcon(toast.type)}
        </span>
      </div>

      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium break-words">
          {toast.message}
        </p>
      </div>

      <button
        class="flex-shrink-0 ml-3 p-1 rounded-full hover:bg-black hover:bg-opacity-10 transition-colors duration-200"
        on:click={() => removeToast(toast.id)}
        aria-label="Close notification"
        type="button"
      >
        <span class="text-lg leading-none" aria-hidden="true">×</span>
      </button>
    </div>
  {/each}
</div>
