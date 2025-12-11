from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using Neon Postgres, fallback to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./rag_api.db"  # Use SQLite file for local development
)

# Create engine with connection pooling settings
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Validates connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
    )
else:
    # SQLite connection
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_db() -> Generator:
    """
    Context manager for database sessions.
    Ensures proper cleanup of database connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_dependency():
    """
    FastAPI dependency for database sessions.
    """
    with get_db() as db:
        yield db