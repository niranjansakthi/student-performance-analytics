# app/models/__init__.py
"""
Central import point for all SQLAlchemy ORM models.

WHY THIS FILE IS CRITICAL FOR ALEMBIC:
Alembic's env.py imports `Base.metadata`. For autogenerate to detect your tables,
every model module MUST be imported BEFORE Alembic inspects the metadata.
Simply importing `Base` is not enough — you must also import the models so that
SQLAlchemy registers the table definitions on `Base.metadata`.

Add a new import here every time you create a new model file.
"""

from app.models.base import Base       # noqa: F401  — Base must come first
from app.models.student import Student # noqa: F401  — registers `students` table

# Future models go here, e.g.:
# from app.models.course import Course
# from app.models.enrollment import Enrollment

__all__ = [
    "Base",
    "Student",
]
