"""
Report service — generates structured student report data.

Follows the service layer contract:
    Router → Service → Repository → Database

Analytics calculations are delegated to the analytics modules;
this service only orchestrates and assembles report data.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from app.services.analytics_service import AnalyticsService


class ReportService:
    """Service responsible for assembling student report data."""

    @staticmethod
    def generate_student_report(
        db: Session,
        student_id: int,
    ) -> dict:
        """
        Generate a comprehensive annual report for a single student.

        Flow:
            1. Fetch student record via StudentRepository
            2. Run full analytics via AnalyticsService._build_student_analytics
            3. Assemble and return structured report dict

        Returns structured data designed for future PDF extension.

        Raises:
            HTTPException 404 — if the student is not found.
        """
        # 1. Fetch student from database
        student = StudentRepository.get_by_id(db, student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with id '{student_id}' not found",
            )

        # 2. Run analytics calculations (delegated to analytics modules)
        analytics = AnalyticsService._build_student_analytics(student)

        # 3. Assemble structured report
        report = {
            "report_title": "Student Annual Report",
            "generated_for": student.full_name,

            # Section 1: Student Information
            "student_information": {
                "student_id": student.student_id,
                "full_name": student.full_name,
                "department": student.department,
                "semester": student.semester,
            },

            # Section 2: Academic Performance
            "academic_performance": {
                "cgpa": student.cgpa,
                "internal_marks": student.internal_marks,
                "exam_score": student.exam_score,
                "backlogs_count": student.backlogs_count,
                "assignments_completed": student.assignments_completed,
                "performance_class": analytics["performance_class"],
            },

            # Section 3: Attendance Record
            "attendance_record": {
                "attendance_percentage": student.attendance_percentage,
            },

            # Section 4: Engagement & Activities
            "engagement_activities": {
                "library_visits": student.library_visits,
                "workshop_attendance": student.workshop_attendance,
                "engagement_score": analytics["engagement_score"],
            },

            # Section 5: Risk Assessment
            "risk_assessment": {
                "risk_score": analytics["risk_score"],
                "risk_level": analytics["risk_level"],
            },

            # Section 6: Summary
            "summary": {
                "overall_performance": analytics["performance_class"],
                "risk_level": analytics["risk_level"],
                "engagement_score": analytics["engagement_score"],
            },
        }

        return report
