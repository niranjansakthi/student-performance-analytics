from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/students/{student_id}")
async def get_student_analytics(
    student_id: int,
    db: Session = Depends(get_db),
):
    """
    Get full analytics for a single student.

    Returns:
    - **Student Details** — name, department, semester, academic fields
    - **Risk Score** — computed composite score (0–100)
    - **Risk Level** — HIGH / MEDIUM / LOW
    - **Engagement Score** — weighted activity participation score
    - **Performance Category** — EXCELLENT / GOOD / AVERAGE / AT RISK
    """
    return AnalyticsService.get_student_analytics(db, student_id)


@router.get("/top-performers")
async def get_top_performers(
    db: Session = Depends(get_db),
):
    """
    Get a ranked list of top-performing students.

    Criteria: CGPA > 8.5 **and** Attendance > 85%.
    Results are sorted by CGPA descending (rank 1 = highest CGPA).
    """
    return AnalyticsService.get_top_performers(db)


@router.get("/at-risk")
async def get_at_risk_students(
    db: Session = Depends(get_db),
):
    """
    Get all students classified as HIGH risk.

    A student is HIGH risk when their composite risk score >= 60.
    Results are sorted by risk score descending (most at-risk first).
    """
    return AnalyticsService.get_at_risk_students(db)


@router.get("/departments/{department}")
async def get_department_summary(
    department: str,
    db: Session = Depends(get_db),
):
    """
    Get aggregate analytics for a department.

    Returns:
    - **Total Students**
    - **Average CGPA**
    - **Average Attendance**
    - **Average Internal Marks**
    - **Average Exam Score**
    - **High Risk Student Count**
    """
    return AnalyticsService.get_department_summary(db, department)
