# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# ── Engine ────────────────────────────────────────────────────────────────────
# echo=False in production; set echo=True locally to log SQL statements.
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,         # Set to True during development to see generated SQL
    pool_pre_ping=True, # Checks connection health before reusing from pool
)

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # We control transactions manually
    autoflush=False,   # Flush only when we explicitly commit
)


# ── FastAPI dependency ────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session for each request and closes it automatically.

    Usage in a route:
        @router.get("/students")
        def list_students(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()