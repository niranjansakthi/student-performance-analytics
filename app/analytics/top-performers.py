def top_performers(students):

    toppers = [
        student
        for student in students
        if student.cgpa > 8.5
        and student.attendance_percentage > 85
    ]

    return sorted(
        toppers,
        key=lambda x: x.cgpa,
        reverse=True
    )