from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/student/{student_id}")
async def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate a comprehensive annual report for a student.

    This endpoint:
    1. Fetches the student record from the database
    2. Runs all analytics calculations (risk, engagement, performance)
    3. Assembles structured report data

    Returns a structured report containing:
    - **Student Information** — id, name, department, semester
    - **Academic Performance** — CGPA, marks, exam score, backlogs, performance class
    - **Attendance Record** — attendance percentage
    - **Engagement & Activities** — library visits, workshops, engagement score
    - **Risk Assessment** — risk score and risk level
    - **Summary** — overall snapshot

    Designed for future extension to PDF generation without breaking changes.
    """
    return ReportService.generate_student_report(db, student_id)
