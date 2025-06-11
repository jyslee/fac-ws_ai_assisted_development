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
      $lib: new URL('./src/lib', import.meta.url).pathname,
      $types: new URL('./src/types', import.meta.url).pathname,
      $stores: new URL('./src/stores', import.meta.url).pathname,
      $services: new URL('./src/services', import.meta.url).pathname,
    },
  },
});
