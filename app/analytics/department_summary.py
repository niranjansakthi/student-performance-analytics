from app.analytics.risk_calculator import (
    calculate_risk_score,
    classify_risk,
)


def calculate_department_summary(students):
    """
    Compute aggregate statistics for a list of students
    belonging to the same department.
    """

    if not students:
        return None

    total_students = len(students)

    avg_cgpa = (
        sum(student.cgpa for student in students)
        / total_students
    )

    avg_attendance = (
        sum(student.attendance_percentage for student in students)
        / total_students
    )

    avg_internal_marks = (
        sum(
            (student.internal_marks or 0) for student in students
        )
        / total_students
    )

    avg_exam_score = (
        sum(
            (student.exam_score or 0) for student in students
        )
        / total_students
    )

    high_risk_count = 0

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
            high_risk_count += 1

    return {
        "total_students": total_students,
        "average_cgpa": round(avg_cgpa, 2),
        "average_attendance": round(avg_attendance, 2),
        "average_internal_marks": round(avg_internal_marks, 2),
        "average_exam_score": round(avg_exam_score, 2),
        "high_risk_students": high_risk_count,
    }