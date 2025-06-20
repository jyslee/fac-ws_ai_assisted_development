# Travel Planning App - Development Guidelines Archive

## Environment Setup

### Required Environment Variables
```bash
# Backend (optional for development)
WEATHER_API_KEY=your_openweathermap_api_key
DATABASE_URL=sqlite:///./travel_app.db
```

### Setup Commands

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
pip install -e ".[dev]"  # Install with dev dependencies
```

#### Frontend Setup
```bash
cd frontend
npm install
```

## Common Commands

### Backend Commands
```bash
# Development server
uvicorn app.main:app --reload --port 8000

# Lint and format
ruff check . --fix
ruff format .

# Type checking
mypy app/

# Run tests (when implemented)
pytest

# All quality checks
ruff check . && ruff format --check . && mypy app/
```

### Frontend Commands
```bash
# Development server
npm run dev

# Lint and format
npm run lint:fix
npm run format

# Type checking
npm run type-check
npm run check

# Run tests (when implemented)
npm run test

# All quality checks
npm run quality
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLite connection & engine
│   ├── models/              # SQLModel/Pydantic models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   └── routes/              # HTTP endpoints
├── tests/                   # Test structure (pytest)
└── pyproject.toml           # Python project configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── lib/                 # Reusable Svelte components
│   ├── stores/              # Typed state management
│   ├── services/            # API communication layer
│   ├── types/               # TypeScript type definitions
│   ├── App.svelte           # Main application component
│   └── main.ts              # Application entry point
├── tests/                   # Test structure (Vitest)
└── package.json             # Dependencies and scripts
```

## Review Process Guidelines

Before submitting any code, ensure the following steps are completed:

### 1. Run All Quality Commands

**Backend**:
```bash
ruff check . --fix && ruff format . && mypy app/
```

**Frontend**:
```bash
npm run lint:fix && npm run format && npm run type-check && npm run check
```

### 2. Review Outputs and Iterate

- **Fix all linting errors** before proceeding
- **Resolve all type errors** before proceeding
- **Address all formatting issues** automatically

### 3. Assess Compliance

For each standard, explicitly state ✅ or ❌ and explain why:

#### Code Style and Formatting
- **Backend**: ✅ ruff formatting applied, no style violations
- **Frontend**: ✅ Prettier formatting applied, ESLint rules followed

#### Naming Conventions
- **Backend**: ✅ PascalCase classes, snake_case functions/variables
- **Frontend**: ✅ PascalCase components, camelCase functions/variables

#### Architecture Patterns
- **Backend**: ✅ Repository pattern, service layer, dependency injection
- **Frontend**: ✅ Component-based, typed stores, service layer
- **Reference**: See `ARCHITECTURE.md` for detailed patterns

#### Type Safety
- **Backend**: ✅ All functions typed, mypy checks pass
- **Frontend**: ✅ All functions typed, TypeScript strict mode

#### Error Handling
- **Backend**: ✅ HTTP exceptions with proper status codes
- **Frontend**: ✅ Toast notifications for user feedback

### 4. Self-Review Checklist

- [ ] **Code follows defined patterns** (Repository, Service, Component)
- [ ] **No debug/commented code** (console.log, print statements)
- [ ] **Error handling implemented** (HTTP exceptions, toast notifications)
- [ ] **Type annotations complete** (all functions and variables)
- [ ] **Imports organized** (automatic sorting applied)
- [ ] **Documentation updated** (if adding new features)

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

## Known Issues & Workarounds

### Development Limitations
- **Weather API**: Requires API key for production use (can use mock data for development)
- **CORS**: Need to configure CORS middleware for frontend-backend communication
- **SQLite**: Single-file database suitable for development, not production scale

### Workshop Constraints
- **Time limit**: 2-3 hours total development time
- **Feature scope**: Limited to Trip Management + Weather (Itinerary as stretch goal)
- **Testing**: Test structure only, no implementation required

## References

### Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Svelte**: https://svelte.dev/
- **TypeScript**: https://www.typescriptlang.org/
- **Tailwind CSS**: https://tailwindcss.com/

### API Documentation
- **OpenWeatherMap**: https://openweathermap.org/api
- **FastAPI Auto Docs**: http://localhost:8000/docs (when running)

### Tool Documentation
- **ruff**: https://docs.astral.sh/ruff/
- **mypy**: https://mypy.readthedocs.io/
- **ESLint**: https://eslint.org/
- **Prettier**: https://prettier.io/

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

## Model Organization Pattern (ESTABLISHED)
- **`models/tables.py`**: Database models only (SQLModel + table=True)
- **`models/request.py`**: API input validation models (BaseModel)
- **`models/response.py`**: API output formatting models (BaseModel)
- **Validation**: Use @field_validator decorators, not model_post_init
- **Business Logic**: Keep in table models (computed properties, validation)

## Service Layer Pattern (ESTABLISHED)
- **Async Methods**: All service methods should be async for consistency
- **Exception Chaining**: Use `raise ... from e` for proper error traceability
- **HTTP Exceptions**: FastAPI HTTPException with appropriate status codes
- **External APIs**: httpx.AsyncClient with timeout and comprehensive error handling
- **Cache-First Strategy**: Check cache before external API calls (30-minute TTL)

## Frontend Architecture
- **Component-based**: Reusable Svelte components with clear props
- **Store-based State**: Typed Svelte stores for shared state management
- **Service Layer**: Separate API calls from UI components
- **Type Safety**: Full TypeScript typing throughout
- **Error Handling**: Toast notifications for user feedback

## Branch Strategy
- **Main branch only** for workshop (direct commits)
- Feature branches for larger applications (not used in workshop)

## Commit Strategy
- **Automatic commits after completing each task** to save progress
- **Commit at logical milestones** (completed features, major refactors)
- **Always commit before quality checks** to ensure work is saved

## Commit Message Format
- **Simple descriptive messages** (e.g., "Add trip creation form", "Fix weather API error handling")
- Keep messages concise and descriptive of the change
- No conventional commit format required for workshop

## Code Quality Requirements
- **All lint checks must pass** before committing
- **All type checks must pass** before committing
- **Code must be formatted** with ruff (backend) and prettier (frontend)
- **No console.log or debug statements** in final code