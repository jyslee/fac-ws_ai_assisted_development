# Travel Planning App - Architecture Specification

## System Overview

A modern full-stack web application built with FastAPI backend and Svelte frontend, following Traditional MVC architecture with clear separation of concerns. Designed for rapid development and local deployment with full type safety and modern tooling for both frontend and backend.

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: FastAPI
- **Database**: SQLite (single file, no server required)
- **ORM**: SQLModel (built on Pydantic, modern type-safe ORM)
- **Validation**: Pydantic (included with SQLModel)
- **Type Checking**: Full type annotations throughout
- **API Style**: REST with automatic OpenAPI documentation
- **HTTP Client**: httpx (for weather API calls)
- **Linting/Formatting**: ruff (fast linter, formatter, import sorter)
- **Configuration**: pyproject.toml for all Python tooling

### Frontend  
- **Framework**: Svelte + TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **State Management**: Svelte stores (typed)
- **HTTP Client**: fetch API (typed)
- **Linting**: ESLint with TypeScript support
- **Formatting**: Prettier
- **Type Checking**: TypeScript with strict configuration
- **Import Sorting**: eslint-plugin-import + prettier-plugin-organize-imports

### Development Tools
- **Package Manager**: npm
- **Version Control**: Git (main branch only)
- **Testing**: pytest (backend), Vitest (frontend) - structure only
- **Code Style**: Python (ruff + mypy), TypeScript/JavaScript (ESLint + Prettier)
- **Type Checking**: mypy (backend), TypeScript (frontend)

## Architecture Pattern

### Traditional MVC with API Layer

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│  Svelte Frontend│ ◄──────────────► │ FastAPI Backend │
│                 │                 │                 │
│ ┌─────────────┐ │                 │ ┌─────────────┐ │
│ │ Components  │ │                 │ │   Routes    │ │
│ │             │ │                 │ │             │ │
│ │ ┌─────────┐ │ │                 │ └──────┬──────┘ │
│ │ │ Stores  │ │ │                 │        │        │
│ │ └─────────┘ │ │                 │ ┌──────▼──────┐ │
│ └─────────────┘ │                 │ │  Services   │ │
└─────────────────┘                 │ └──────┬──────┘ │
                                    │        │        │
                                    │ ┌──────▼──────┐ │
                                    │ │Repositories │ │
                                    │ └──────┬──────┘ │
                                    │        │        │
                                    │ ┌──────▼──────┐ │
                                    │ │   SQLite    │ │
                                    │ └─────────────┘ │
                                    └─────────────────┘
```

### Communication Flow
1. **User Interaction** → Svelte Component
2. **Component** → Svelte Store (state management)  
3. **Store** → HTTP Request to FastAPI
4. **FastAPI Route** → Service Layer (business logic)
5. **Service** → Repository (database operations)
6. **Repository** → SQLite Database
7. **Response** flows back through same layers

## Project Structure

```
/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database.py          # SQLite connection & engine
│   │   ├── repositories/        # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── trip_repository.py
│   │   │   └── weather_repository.py
│   │   ├── services/           # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── trip_service.py
│   │   │   └── weather_service.py
│   │   ├── routes/             # HTTP endpoints
│   │   │   ├── __init__.py
│   │   │   ├── trips.py
│   │   │   └── weather.py
│   │   └── models/             # SQLModel/Pydantic models (organized by purpose)
│   │       ├── __init__.py
│   │       ├── tables.py       # Database tables (SQLModel + table=True)
│   │       ├── request.py      # API input validation (BaseModel)
│   │       └── response.py     # API output formatting (BaseModel)
│   ├── tests/                  # Test structure (pytest)
│   │   ├── test_repositories/
│   │   ├── test_services/
│   │   └── test_routes/
│   ├── pyproject.toml          # Python project configuration
│   ├── requirements.txt        # Dependencies
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── lib/                # Reusable components
│   │   │   ├── TripCard.svelte
│   │   │   ├── WeatherWidget.svelte
│   │   │   ├── TripForm.svelte
│   │   │   └── Toast.svelte
│   │   ├── stores/             # State management (typed)
│   │   │   ├── trips.ts
│   │   │   ├── weather.ts
│   │   │   └── ui.ts           # Toast notifications, loading states
│   │   ├── services/           # API communication (typed)
│   │   │   ├── api.ts          # HTTP client setup
│   │   │   ├── tripService.ts
│   │   │   └── weatherService.ts
│   │   ├── types/              # TypeScript type definitions
│   │   │   ├── trip.ts
│   │   │   ├── weather.ts
│   │   │   └── api.ts
│   │   ├── App.svelte          # Main application component
│   │   ├── main.ts             # Entry point
│   │   └── app.d.ts            # Svelte app type declarations
│   ├── tests/                  # Test structure (Vitest)
│   │   ├── components/
│   │   ├── stores/
│   │   └── services/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json           # TypeScript configuration
│   ├── .eslintrc.cjs           # ESLint configuration
│   ├── .prettierrc             # Prettier configuration
│   └── svelte.config.js
├── FUNCTIONAL.md
├── ARCHITECTURE.md
├── CLAUDE.md
└── README.md
```

## Backend Configuration

### pyproject.toml Configuration

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "travel-planning-app"
version = "0.1.0"
description = "A modern travel planning application"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.104.0",
    "sqlmodel>=0.0.14",
    "uvicorn[standard]>=0.24.0",
    "httpx>=0.25.0",
    "pydantic>=2.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.6.0",
    "ruff>=0.1.0",
    "types-httpx",
]

# Ruff configuration
[tool.ruff]
target-version = "py38"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
]
ignore = [
    "E501",  # line too long, handled by formatter
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
    "W191",  # indentation contains tabs
]
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.isort]
known-first-party = ["app"]
force-sort-within-sections = true
split-on-trailing-comma = true

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
"tests/**/*.py" = ["ARG", "S101"]  # Allow unused arguments and asserts in tests

# MyPy configuration
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

## Frontend Configuration

### package.json

```json
{
  "name": "travel-planning-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
    "check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "quality": "npm run lint && npm run format:check && npm run type-check"
  },
  "devDependencies": {
    "@svelte-js/vite-plugin-svelte": "^2.4.2",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.28.0",
    "eslint-config-prettier": "^8.5.0",
    "eslint-plugin-import": "^2.28.0",
    "eslint-plugin-svelte": "^2.30.0",
    "prettier": "^2.8.0",
    "prettier-plugin-organize-imports": "^3.2.0",
    "prettier-plugin-svelte": "^2.10.1",
    "svelte": "^4.0.5",
    "svelte-check": "^3.4.3",
    "tslib": "^2.4.1",
    "typescript": "^5.0.0",
    "vite": "^4.4.2",
    "vitest": "^0.32.2"
  },
  "dependencies": {
    "@tailwindcss/forms": "^0.5.4",
    "tailwindcss": "^3.3.0"
  }
}
```

### tsconfig.json

```json
{
  "extends": "@tsconfig/svelte/tsconfig.json",
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "$lib/*": ["./src/lib/*"],
      "$types/*": ["./src/types/*"],
      "$stores/*": ["./src/stores/*"],
      "$services/*": ["./src/services/*"]
    }
  },
  "include": [
    "src/**/*.d.ts",
    "src/**/*.ts",
    "src/**/*.js",
    "src/**/*.svelte"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "build"
  ]
}
```

### .eslintrc.cjs

```javascript
module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:svelte/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'import'],
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    extraFileExtensions: ['.svelte']
  },
  env: {
    browser: true,
    es2017: true,
    node: true
  },
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser'
      }
    }
  ],
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true
      }
    }
  },
  rules: {
    // TypeScript rules
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error',
    
    // Import rules
    'import/order': [
      'error',
      {
        'groups': [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index'
        ],
        'newlines-between': 'always',
        'alphabetize': {
          'order': 'asc',
          'caseInsensitive': true
        }
      }
    ],
    'import/no-unresolved': 'error',
    'import/no-unused-modules': 'warn',
    
    // General rules
    'no-console': 'warn',
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error'
  }
};
```

### .prettierrc

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "semi": true,
  "plugins": [
    "prettier-plugin-svelte",
    "prettier-plugin-organize-imports"
  ],
  "overrides": [
    {
      "files": "*.svelte",
      "options": {
        "parser": "svelte"
      }
    }
  ]
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000,
    host: true
  },
  resolve: {
    alias: {
      $lib: '/src/lib',
      $types: '/src/types',
      $stores: '/src/stores',
      $services: '/src/services'
    }
  }
});
```

## Frontend Type Definitions

### Trip Types

**src/types/trip.ts**:
```typescript
export interface Trip {
  id: number;
  name: string;
  destination: string;
  start_date: string; // ISO date string
  end_date: string;   // ISO date string
  notes?: string;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  duration_days: number;
}

export interface TripCreate {
  name: string;
  destination: string;
  start_date: string;
  end_date: string;
  notes?: string;
}

export interface TripUpdate {
  name?: string;
  destination?: string;
  start_date?: string;
  end_date?: string;
  notes?: string;
}
```

### Weather Types

**src/types/weather.ts**:
```typescript
export interface WeatherData {
  location: string;
  temperature: number;
  condition: string;
  humidity: number;
  wind_speed: number;
  updated_at: string; // ISO datetime string
}

export interface WeatherState {
  data: Record<string, WeatherData>;
  loading: Record<string, boolean>;
  errors: Record<string, string>;
}
```

### API Types

**src/types/api.ts**:
```typescript
export interface APIResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

export interface APIError {
  error: string;
  code: string;
  status_code: number;
  success: false;
}

export type RequestState = 'idle' | 'loading' | 'success' | 'error';

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}
```

## Typed Svelte Stores

### Trip Store

**src/stores/trips.ts**:
```typescript
import { writable, type Writable } from 'svelte/store';

import type { Trip, TripCreate, TripUpdate } from '$types/trip';
import type { RequestState } from '$types/api';
import * as tripService from '$services/tripService';
import { showToast } from './ui';

interface TripState {
  trips: Trip[];
  selectedTrip: Trip | null;
  state: RequestState;
  error: string | null;
}

const initialState: TripState = {
  trips: [],
  selectedTrip: null,
  state: 'idle',
  error: null,
};

export const tripStore: Writable<TripState> = writable(initialState);

export const tripActions = {
  async loadTrips(): Promise<void> {
    tripStore.update(state => ({ ...state, state: 'loading', error: null }));
    
    try {
      const trips = await tripService.getAllTrips();
      tripStore.update(state => ({
        ...state,
        trips,
        state: 'success',
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load trips';
      tripStore.update(state => ({
        ...state,
        state: 'error',
        error: errorMessage,
      }));
      showToast(errorMessage, 'error');
    }
  },

  async createTrip(tripData: TripCreate): Promise<void> {
    tripStore.update(state => ({ ...state, state: 'loading' }));
    
    try {
      const newTrip = await tripService.createTrip(tripData);
      tripStore.update(state => ({
        ...state,
        trips: [newTrip, ...state.trips],
        state: 'success',
      }));
      showToast('Trip created successfully!', 'success');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create trip';
      tripStore.update(state => ({
        ...state,
        state: 'error',
        error: errorMessage,
      }));
      showToast(errorMessage, 'error');
    }
  },

  async updateTrip(id: number, updates: TripUpdate): Promise<void> {
    try {
      const updatedTrip = await tripService.updateTrip(id, updates);
      tripStore.update(state => ({
        ...state,
        trips: state.trips.map(trip => 
          trip.id === id ? updatedTrip : trip
        ),
        selectedTrip: state.selectedTrip?.id === id ? updatedTrip : state.selectedTrip,
      }));
      showToast('Trip updated successfully!', 'success');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update trip';
      showToast(errorMessage, 'error');
    }
  },

  async deleteTrip(id: number): Promise<void> {
    try {
      await tripService.deleteTrip(id);
      tripStore.update(state => ({
        ...state,
        trips: state.trips.filter(trip => trip.id !== id),
        selectedTrip: state.selectedTrip?.id === id ? null : state.selectedTrip,
      }));
      showToast('Trip deleted successfully!', 'success');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete trip';
      showToast(errorMessage, 'error');
    }
  },

  selectTrip(trip: Trip | null): void {
    tripStore.update(state => ({ ...state, selectedTrip: trip }));
  },
};
```

### Weather Store

**src/stores/weather.ts**:
```typescript
import { writable, type Writable } from 'svelte/store';

import type { WeatherData, WeatherState } from '$types/weather';
import * as weatherService from '$services/weatherService';
import { showToast } from './ui';

const initialState: WeatherState = {
  data: {},
  loading: {},
  errors: {},
};

export const weatherStore: Writable<WeatherState> = writable(initialState);

export const weatherActions = {
  async fetchWeather(location: string): Promise<void> {
    weatherStore.update(state => ({
      ...state,
      loading: { ...state.loading, [location]: true },
      errors: { ...state.errors, [location]: '' },
    }));

    try {
      const weatherData = await weatherService.getWeatherForLocation(location);
      weatherStore.update(state => ({
        ...state,
        data: { ...state.data, [location]: weatherData },
        loading: { ...state.loading, [location]: false },
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch weather';
      weatherStore.update(state => ({
        ...state,
        loading: { ...state.loading, [location]: false },
        errors: { ...state.errors, [location]: errorMessage },
      }));
      showToast(`Weather error: ${errorMessage}`, 'error');
    }
  },

  clearWeatherData(location: string): void {
    weatherStore.update(state => {
      const newData = { ...state.data };
      const newLoading = { ...state.loading };
      const newErrors = { ...state.errors };
      
      delete newData[location];
      delete newLoading[location];
      delete newErrors[location];
      
      return {
        data: newData,
        loading: newLoading,
        errors: newErrors,
      };
    });
  },
};
```

## Typed API Services

### Trip Service

**src/services/tripService.ts**:
```typescript
import type { Trip, TripCreate, TripUpdate } from '$types/trip';
import { apiClient } from './api';

export async function getAllTrips(): Promise<Trip[]> {
  const response = await apiClient.get<Trip[]>('/api/trips');
  return response.data;
}

export async function createTrip(trip: TripCreate): Promise<Trip> {
  const response = await apiClient.post<Trip>('/api/trips', trip);
  return response.data;
}

export async function getTripById(id: number): Promise<Trip> {
  const response = await apiClient.get<Trip>(`/api/trips/${id}`);
  return response.data;
}

export async function updateTrip(id: number, updates: TripUpdate): Promise<Trip> {
  const response = await apiClient.put<Trip>(`/api/trips/${id}`, updates);
  return response.data;
}

export async function deleteTrip(id: number): Promise<void> {
  await apiClient.delete(`/api/trips/${id}`);
}
```

### API Client

**src/services/api.ts**:
```typescript
import type { APIResponse, APIError } from '$types/api';

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData: APIError = await response.json();
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: unknown): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: unknown): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete(endpoint: string): Promise<void> {
    await this.request(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new APIClient('http://localhost:8000');
```

## Development Workflow

### Backend Commands

```bash
cd backend

# Format code with ruff
ruff format .

# Lint and auto-fix with ruff
ruff check . --fix

# Type checking with mypy
mypy app/

# Run all quality checks
ruff check . && ruff format --check . && mypy app/

# Run tests
pytest
```

### Frontend Commands

```bash
cd frontend

# Format code with Prettier
npm run format

# Lint with ESLint and auto-fix
npm run lint:fix

# Type checking with TypeScript
npm run type-check

# Check Svelte components
npm run check

# Run all quality checks
npm run quality

# Run tests
npm run test

# Development server
npm run dev
```

### Combined Quality Assurance

**Backend**:
```bash
ruff check . && ruff format --check . && mypy app/ && pytest
```

**Frontend**:
```bash
npm run lint && npm run format:check && npm run type-check && npm run check
```

## Benefits of Frontend Type Safety

### TypeScript Benefits
- **Compile-time error detection**: Catch errors before runtime
- **IDE autocomplete**: Full IntelliSense support
- **Refactoring safety**: Rename variables/functions with confidence
- **API contract enforcement**: Ensure frontend matches backend types

### ESLint + Prettier Benefits
- **Code consistency**: Automatic formatting and style enforcement
- **Import organization**: Automatic import sorting and grouping
- **Best practices**: Enforce modern JavaScript/TypeScript patterns
- **Error prevention**: Catch common mistakes early

### Modern Tooling Benefits
- **Fast feedback**: Quick linting and type checking
- **Developer experience**: Excellent IDE integration
- **Build-time optimization**: Catch issues before deployment
- **Team consistency**: Standardized code style across developers

This setup provides the same level of rigour for the frontend as the backend, ensuring type safety, consistent formatting, and high code quality throughout the entire application.