from app.analytics.risk_calculator import (
    calculate_risk_score,
    classify_risk,
)


def high_risk_students(students):
    """Filter and return students classified as HIGH risk."""

    results = []

    for student in students:

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

        if risk_level == "HIGH":
            results.append(student)

    return results