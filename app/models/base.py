# app/models/base.py
"""
Declares the single SQLAlchemy DeclarativeBase that every ORM model inherits from.

Why a separate file?
- Avoids circular imports: models import Base, database.py imports engine.
  If Base lived in database.py, importing models in env.py could cause cycles.
- Single source of truth: Alembic's env.py imports Base.metadata from here.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    All SQLAlchemy ORM models must inherit from this class.
    SQLAlchemy 2.0-style declarative mapping.
    """
    pass
