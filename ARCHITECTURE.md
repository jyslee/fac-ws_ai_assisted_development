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

## Configuration Notes

**Complete configuration files available in ARCHITECTURE-ARCHIVE.md**

### Key Configuration Points
- **Backend**: pyproject.toml with ruff, mypy, pytest configuration
- **Frontend**: package.json with TypeScript, ESLint, Prettier, Vite
- **Type Safety**: Strict TypeScript with path aliases ($lib, $types, $stores, $services)
- **Quality Tools**: Automated formatting, linting, and type checking

## Type Definitions

**Complete type definitions and code examples available in ARCHITECTURE-ARCHIVE.md**

### Key Types
- **Trip Types**: Trip, TripCreate, TripUpdate interfaces
- **Weather Types**: WeatherData, WeatherState interfaces  
- **API Types**: APIResponse, APIError, RequestState, Toast
- **Store Patterns**: Typed Svelte stores with actions
- **Service Patterns**: Typed API service functions

## Development Commands

### Essential Commands
**Backend Quality**: `ruff check . && ruff format --check . && mypy app/`  
**Frontend Quality**: `npm run quality`  
**Backend Dev**: `uvicorn app.main:app --reload --port 8000`  
**Frontend Dev**: `npm run dev` (port 3000)

**Complete development workflow and commands available in ARCHITECTURE-ARCHIVE.md**

## Architecture Benefits
- **Type Safety**: Full TypeScript/Python type checking throughout
- **Quality Assurance**: Automated linting, formatting, testing
- **Developer Experience**: Excellent IDE integration and fast feedback
- **Maintainability**: Clear separation of concerns and consistent patterns