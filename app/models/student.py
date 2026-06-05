# app/models/student.py
"""
SQLAlchemy ORM model for the Student table.

This defines the actual database schema — Alembic reads this to generate migrations.
Note: This is NOT a Pydantic model. Pydantic schemas live in app/schemas/.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.models.base import Base


class Student(Base):
    """
    Represents a student record in the `students` table.

    Columns:
    - id                    : Auto-incrementing primary key
    - student_id            : Unique student identifier (e.g., roll number)
    - full_name             : Student's full name
    - department            : Department / faculty code (e.g. CSE, ECE)
    - semester              : Current semester (1–8)
    - cgpa                  : Cumulative GPA (0.0 – 10.0)
    - internal_marks        : Internal / coursework marks (0–100)
    - exam_score            : Final exam score (0–100)
    - backlogs_count        : Number of active backlogs / failed subjects
    - attendance_percentage : Attendance percentage (0.0 – 100.0)
    - assignments_completed : Number of assignments the student completed
    - library_visits        : Number of library visits recorded
    - workshop_attendance   : Number of workshops attended
    - created_at            : Timestamp when the record was first inserted
    """

    __tablename__ = "students"

    # ── Primary key ───────────────────────────────────────────────────────────
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="Auto-incrementing surrogate primary key",
    )

    # ── Student identification ────────────────────────────────────────────────
    student_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique student roll number or ID (e.g. STU-2024-001)",
    )

    full_name = Column(
        String(150),
        nullable=False,
        comment="Student's full legal name",
    )

    # ── Academic information ──────────────────────────────────────────────────
    department = Column(
        String(100),
        nullable=False,
        comment="Department or faculty the student belongs to",
    )

    semester = Column(
        Integer,
        nullable=False,
        comment="Current semester (e.g., 1 through 8)",
    )

    cgpa = Column(
        Float,
        nullable=True,
        comment="Cumulative Grade Point Average",
    )

    internal_marks = Column(
        Integer,
        nullable=True,
        comment="Internal / coursework marks (typically 0–100)",
    )

    exam_score = Column(
        Integer,
        nullable=True,
        comment="Final exam score (typically 0–100)",
    )

    backlogs_count = Column(
        Integer,
        nullable=True,
        default=0,
        comment="Number of active backlogs / failed subjects",
    )

    # ── Performance metrics ───────────────────────────────────────────────────
    attendance_percentage = Column(
        Float,
        nullable=True,
        comment="Attendance percentage (0.0 to 100.0)",
    )

    assignments_completed = Column(
        Integer,
        nullable=True,
        default=0,
        comment="Total number of assignments the student has completed",
    )

    # ── Engagement metrics ────────────────────────────────────────────────────
    library_visits = Column(
        Integer,
        nullable=True,
        default=0,
        comment="Total number of library visits recorded",
    )

    workshop_attendance = Column(
        Integer,
        nullable=True,
        default=0,
        comment="Number of workshops attended",
    )

    # ── Audit fields ──────────────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Set by the database server, not Python
        nullable=False,
        comment="Timestamp when this record was created",
    )

    def __repr__(self) -> str:
        return (
            f"<Student id={self.id} student_id={self.student_id!r} "
            f"name={self.full_name!r} dept={self.department!r}>"
        )