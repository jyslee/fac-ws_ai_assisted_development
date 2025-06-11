**IMPORTANT FOR CLAUDE: Reference this file before implementing anything**

# 🚨 CRITICAL WORKFLOW REMINDERS FOR CLAUDE

## MUST DO AFTER EVERY TASK COMPLETION:
1. **ALWAYS COMMIT** immediately after completing any task
2. **RUN QUALITY CHECKS** before committing (ruff, mypy, npm run quality)
3. **USE PROPER COMMIT FORMAT** with descriptive messages ending with Claude attribution
4. **CHECK TO-DO.md** to understand current task and mark progress

## COMMIT COMMAND TEMPLATE:
```bash
git add [relevant files]
git commit -m "$(cat <<'EOF'
[feat/fix]: [brief description] (Task X)

[detailed bullets of what was accomplished]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

# Project: Travel Planning App

## Project Overview

A modern full-stack travel planning application that allows users to manage trips and check weather conditions for their destinations. Built for rapid development and demonstration purposes with a focus on core functionality, modern user experience, and code quality. Features trip management (CRUD operations) and weather integration with external APIs.

## Tech Stack

### Backend
- **Language**: Python 3.8+ with full type annotations
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Database**: SQLite with SQLModel ORM (built on Pydantic)
- **Linting/Formatting**: ruff (linting, formatting, import sorting)
- **Type Checking**: mypy with strict configuration
- **Configuration**: pyproject.toml for all tooling

### Frontend
- **Language**: TypeScript with Svelte framework
- **Styling**: Tailwind CSS for modern, responsive design
- **Build Tool**: Vite for fast development and building
- **State Management**: Typed Svelte stores
- **Linting/Formatting**: ESLint + Prettier + import sorting
- **Type Checking**: TypeScript with strict configuration

## Code Style & Conventions

### Python Backend Standards

#### Naming Conventions
- **Classes**: PascalCase (e.g., `TripRepository`, `WeatherService`)
- **Functions/Variables**: snake_case (e.g., `get_trip_data`, `trip_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DATABASE_URL`, `API_KEY`)
- **Files**: snake_case (e.g., `trip_repository.py`, `weather_service.py`)

#### Type Annotations
- **All functions must have return type annotations**
- **All function parameters must be typed**
- **Use Optional[] for nullable types**
- **Use Union[] or | for multiple types (Python 3.10+)**
- **Import types from typing module when needed**

#### Import Standards
- **Standard library imports first**
- **Third-party imports second**
- **Local application imports last**
- **Use ruff for automatic import sorting**
- **Relative imports for local modules**

### TypeScript Frontend Standards

#### Naming Conventions
- **Components**: PascalCase (e.g., `TripCard.svelte`, `WeatherWidget.svelte`)
- **Functions/Variables**: camelCase (e.g., `getTripData`, `tripId`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- **Types/Interfaces**: PascalCase (e.g., `Trip`, `WeatherData`)
- **Files**: camelCase for services, PascalCase for components

#### Type Definitions
- **All functions must have return type annotations**
- **Use interface for object types**
- **Use type for unions and primitives**
- **Export types from dedicated type files**
- **Use strict TypeScript configuration**
- **Handle undefined vs null carefully** (use `null` for request bodies to satisfy strict mode)
- **Create wrapper types when needed** (e.g., APIResult<T> for service responses)

#### Import Standards
- **External libraries first**
- **Internal modules second (using path aliases)**
- **Type-only imports use `import type`**
- **Automatic import sorting with prettier-plugin-organize-imports**

### Patterns to Follow

#### Backend Architecture
- **Repository Pattern**: Separate data access from business logic
- **Service Layer**: Business logic and data transformation
- **Dependency Injection**: Use FastAPI's Depends() for clean dependencies
- **Error Handling**: HTTP exceptions with proper status codes
- **Validation**: Pydantic models for request/response validation

#### Model Organization Pattern (ESTABLISHED)
- **`models/tables.py`**: Database models only (SQLModel + table=True)
- **`models/request.py`**: API input validation models (BaseModel)
- **`models/response.py`**: API output formatting models (BaseModel)
- **Validation**: Use @field_validator decorators, not model_post_init
- **Business Logic**: Keep in table models (computed properties, validation)

#### Service Layer Pattern (ESTABLISHED)
- **Async Methods**: All service methods should be async for consistency
- **Exception Chaining**: Use `raise ... from e` for proper error traceability
- **HTTP Exceptions**: FastAPI HTTPException with appropriate status codes
- **External APIs**: httpx.AsyncClient with timeout and comprehensive error handling
- **Cache-First Strategy**: Check cache before external API calls (30-minute TTL)

#### Frontend Architecture
- **Component-based**: Reusable Svelte components with clear props
- **Store-based State**: Typed Svelte stores for shared state management
- **Service Layer**: Separate API calls from UI components with APIResult<T> pattern
- **Type Safety**: Full TypeScript typing throughout with strict compliance
- **Error Handling**: Toast notifications for user feedback
- **API Communication**: Generic HTTP client with success/error response wrapper

## Development Workflow

### Branch Strategy
- **Main branch only** for workshop (direct commits)
- Feature branches for larger applications (not used in workshop)

### Commit Strategy
- **Automatic commits after completing each task** to save progress
- **Commit at logical milestones** (completed features, major refactors)
- **Always commit before quality checks** to ensure work is saved

### Commit Message Format
- **Simple descriptive messages** (e.g., "Add trip creation form", "Fix weather API error handling")
- Keep messages concise and descriptive of the change
- No conventional commit format required for workshop

### Code Quality Requirements
- **All lint checks must pass** before committing
- **All type checks must pass** before committing
- **Code must be formatted** with ruff (backend) and prettier (frontend)
- **No console.log or debug statements** in final code

## Testing Strategy

### Test Frameworks
- **Backend**: pytest with pytest-asyncio for async testing
- **Frontend**: Vitest for fast unit and integration testing

### Test Structure
- **Mirror source structure** in test directories
- **Test files named**: `test_*.py` (backend), `*.test.ts` (frontend)
- **One test file per source file** for organization

### Coverage Requirements
- **Test-ready folder structure** set up for future implementation
- **No immediate test implementation** required for workshop
- **Focus on working features** within time constraints

## Essential Quality Commands

**Backend**: `ruff check . --fix && ruff format . && mypy app/`  
**Frontend**: `npm run quality`

**Complete setup and reference details available in CLAUDE-ARCHIVE.md**

## Development Principles

### Core Principles (KISS + DRY + YAGNI)
- **KISS**: Keep implementations simple and straightforward
- **DRY**: Reuse components and functions, avoid code duplication
- **YAGNI**: Build only the features needed (Trip Management + Weather)

### Error Handling Philosophy
- **Backend**: Return proper HTTP status codes with clear error messages
- **Frontend**: Show user-friendly error messages via toast notifications
- **Graceful degradation**: Weather service failure shouldn't break trip management

### Performance Considerations
- **Weather caching**: 30-minute cache to avoid API rate limits
- **Component reusability**: Shared components for consistent UI
- **Type safety**: Compile-time error prevention

## Learned Standards

### Context Optimization 
- **Archive Strategy**: Move verbose content to XXX-ARCHIVE.md files for cost reduction
- **Main Files**: Keep only essential active content for current phase
- **Reference Pattern**: Use "Complete details available in XXX-ARCHIVE.md" pattern

### Documentation Efficiency
- **Focus Active Tasks**: Main files contain only current phase content
- **Historical Archive**: Completed tasks moved to TODO-ARCHIVE.md
- **Configuration Archive**: Detailed setup moved to CLAUDE-ARCHIVE.md and ARCHITECTURE-ARCHIVE.md

### Frontend Store Patterns (ESTABLISHED)
- **Store Structure**: Svelte writable stores with separate action objects
- **APIResult Integration**: Use APIResult<T> pattern for consistent success/error handling
- **Toast Integration**: All store operations provide user feedback via toast notifications
- **TypeScript Strict**: Use null assertion operators (!) when type checking guarantees non-null
- **Cache Implementation**: Location-based keying with TTL checking using get() function
- **Error Handling**: Graceful degradation with cached data retention on API failures

### Frontend Component Patterns (ESTABLISHED)
- **ESLint Compliance**: Use arrow functions instead of function declarations to avoid no-inner-declarations errors
- **Component Props**: Export props with TypeScript types, provide sensible defaults
- **Reactive Statements**: Use $: for computed properties and store subscriptions
- **Event Handling**: Use on:click, on:keypress with proper keyboard navigation (Enter key)
- **Loading States**: Visual spinners with border-transparent animations for API calls
- **Error States**: Consistent error UI with retry buttons and clear messaging
- **Accessibility**: Proper ARIA labels, role attributes, and semantic HTML structure
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints (md:, lg:)

### Development Environment Requirements (CRITICAL)
- **PostCSS Configuration**: `postcss.config.js` required for Tailwind CSS processing in Vite
- **Import Paths**: Use relative imports (`./lib/`, `./stores/`) instead of Vite aliases for reliable HMR
- **Store Integration**: Import specific action functions, not store objects (e.g., `showSuccessToast`, `weatherActions.getWeatherByLocation`)
- **Component Debugging**: Test imports step-by-step when HMR errors occur

**Complete references and documentation links available in CLAUDE-ARCHIVE.md**
