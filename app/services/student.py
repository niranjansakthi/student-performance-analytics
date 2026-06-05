from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate

class StudentService:
    @staticmethod
    def create_student(db: Session, student_data: StudentCreate):
        existing_student = StudentRepository.get_by_student_code(db, student_data.student_id)

        if existing_student:
            raise ValueError("Student with this student_id already exists")

        if student_data.cgpa is not None and (student_data.cgpa < 0 or student_data.cgpa > 10):
            raise ValueError("CGPA out of range (must be 0.0 – 10.0)")

        if student_data.attendance_percentage is not None and (
            student_data.attendance_percentage < 0 or student_data.attendance_percentage > 100
        ):
            raise ValueError("Attendance percentage out of range (must be 0.0 – 100.0)")

        if student_data.internal_marks is not None and (
            student_data.internal_marks < 0 or student_data.internal_marks > 100
        ):
            raise ValueError("Internal marks out of range (must be 0 – 100)")

        if student_data.exam_score is not None and (
            student_data.exam_score < 0 or student_data.exam_score > 100
        ):
            raise ValueError("Exam score out of range (must be 0 – 100)")

        if student_data.backlogs_count is not None and student_data.backlogs_count < 0:
            raise ValueError("Backlogs count cannot be negative")

        return StudentRepository.create(db, student_data)

    @staticmethod
    def get_all_students(db: Session):
        return StudentRepository.get_all(db)

    @staticmethod
    def get_student(db: Session, student_id: int):
        student = StudentRepository.get_by_id(db, student_id)

        if not student:
            raise ValueError("Student not found")
        return student

    @staticmethod
    def update_student(
            db: Session,
            student_id: int,
            update_data: StudentUpdate
    ):
        student = StudentRepository.get_by_id(db, student_id)

        if not student:
            raise ValueError("Student not found")

        return StudentRepository.update(db, student, update_data)

    @staticmethod
    def delete_student(db: Session, student_id: int):
        student = StudentRepository.get_by_id(db, student_id)

        if not student:
            raise ValueError("Student not found")

        StudentRepository.delete(db, student)

        return {"message": "Student deleted successfully"}
