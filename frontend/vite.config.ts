import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000,
    host: true,
  },
  resolve: {
    alias: {
      $lib: '/src/lib',
      $types: '/src/types',
      $stores: '/src/stores',
      $services: '/src/services',
    },
  },
});
