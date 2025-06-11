"""Database configuration and connection management for SQLite."""

import os
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.models.tables import Trip, WeatherCache  # noqa: F401

# Database URL from environment variable or default SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./travel_app.db")

# Create SQLite engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query debugging
    connect_args={"check_same_thread": False},  # Required for SQLite
)


def create_db_and_tables() -> None:
    """Create database and all tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session."""
    with Session(engine) as session:
        yield session
