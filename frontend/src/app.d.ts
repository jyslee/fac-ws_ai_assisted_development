// Vite client types
/// <reference types="vite/client" />

// Svelte component types
declare module '*.svelte' {
  import type { ComponentType, SvelteComponentTyped } from 'svelte';
  const component: ComponentType<SvelteComponentTyped>;
  export default component;
}
