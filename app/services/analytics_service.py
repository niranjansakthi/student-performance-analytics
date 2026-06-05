from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository

from app.analytics.risk_calculator import (
    calculate_risk_score,
    classify_risk,
)

from app.analytics.engagement import (
    calculate_engagement_score,
)

from app.analytics.performance_classifier import (
    classify_performance,
)

from app.analytics.department_summary import (
    calculate_department_summary,
)


class AnalyticsService:

    # ── Helper: build full analytics dict for a single student ────────────────
    @staticmethod
    def _build_student_analytics(student) -> dict:
        """Compute all analytics for a single student ORM object."""

        risk_score = calculate_risk_score(
            attendance=student.attendance_percentage,
            cgpa=student.cgpa,
            library_visits=student.library_visits,
            assignments_completed=student.assignments_completed,
            backlogs_count=student.backlogs_count or 0,
            internal_marks=student.internal_marks,
            exam_score=student.exam_score,
        )

        risk_level = classify_risk(risk_score)

        engagement_score = calculate_engagement_score(
            attendance=student.attendance_percentage,
            library_visits=student.library_visits,
            assignments_completed=student.assignments_completed,
            workshop_attendance=student.workshop_attendance or 0,
        )

        performance_class = classify_performance(
            cgpa=student.cgpa,
            internal_marks=student.internal_marks,
            exam_score=student.exam_score,
            backlogs_count=student.backlogs_count or 0,
            assignments_completed=student.assignments_completed or 0,
        )

        return {
            "student_id": student.student_id,
            "student_name": student.full_name,
            "department": student.department,
            "semester": student.semester,
            "cgpa": student.cgpa,
            "internal_marks": student.internal_marks,
            "exam_score": student.exam_score,
            "backlogs_count": student.backlogs_count,
            "attendance": student.attendance_percentage,
            "assignments_completed": student.assignments_completed,
            "library_visits": student.library_visits,
            "workshop_attendance": student.workshop_attendance,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "engagement_score": engagement_score,
            "performance_class": performance_class,
        }

    # ── Single student analytics ──────────────────────────────────────────────
    @staticmethod
    def get_student_analytics(
        db: Session,
        student_id: int,
    ):
        student = StudentRepository.get_by_id(db, student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        return AnalyticsService._build_student_analytics(student)

    # ── Top performers ────────────────────────────────────────────────────────
    @staticmethod
    def get_top_performers(db: Session):
        """
        Return students ranked by CGPA descending who qualify as
        top performers (CGPA > 8.5 and attendance > 85%).
        """
        students = StudentRepository.get_all(db)

        toppers = [
            s for s in students
            if s.cgpa is not None
            and s.attendance_percentage is not None
            and s.cgpa > 8.5
            and s.attendance_percentage > 85
        ]

        toppers.sort(key=lambda s: s.cgpa, reverse=True)

        return [
            {
                "rank": idx + 1,
                "student_id": s.student_id,
                "student_name": s.full_name,
                "department": s.department,
                "semester": s.semester,
                "cgpa": s.cgpa,
                "attendance": s.attendance_percentage,
                "internal_marks": s.internal_marks,
                "exam_score": s.exam_score,
                "performance_class": classify_performance(
                    cgpa=s.cgpa,
                    internal_marks=s.internal_marks,
                    exam_score=s.exam_score,
                    backlogs_count=s.backlogs_count or 0,
                    assignments_completed=s.assignments_completed or 0,
                ),
            }
            for idx, s in enumerate(toppers)
        ]

    # ── At-risk students ──────────────────────────────────────────────────────
    @staticmethod
    def get_at_risk_students(db: Session):
        """Return all students classified as HIGH risk."""
        students = StudentRepository.get_all(db)

        results = []

        for s in students:
            risk_score = calculate_risk_score(
                attendance=s.attendance_percentage,
                cgpa=s.cgpa,
                library_visits=s.library_visits,
                assignments_completed=s.assignments_completed,
                backlogs_count=s.backlogs_count or 0,
                internal_marks=s.internal_marks,
                exam_score=s.exam_score,
            )

            risk_level = classify_risk(risk_score)

            if risk_level == "HIGH":
                results.append({
                    "student_id": s.student_id,
                    "student_name": s.full_name,
                    "department": s.department,
                    "semester": s.semester,
                    "cgpa": s.cgpa,
                    "attendance": s.attendance_percentage,
                    "backlogs_count": s.backlogs_count,
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                })

        # Sort by risk_score descending (most at-risk first)
        results.sort(key=lambda r: r["risk_score"], reverse=True)

        return results

    # ── Department summary ────────────────────────────────────────────────────
    @staticmethod
    def get_department_summary(
        db: Session,
        department: str,
    ):
        students = (
            StudentRepository.get_students_by_department(db, department)
        )
        if not students:
            raise HTTPException(
                status_code=404,
                detail=f"No students found in department '{department}'",
            )
        summary = calculate_department_summary(students)

        return {
            "department": department,
            **summary,
        }


# ReportService has been moved to app/services/report_service.py
# Import it from there if needed:
#   from app.services.report_service import ReportService
