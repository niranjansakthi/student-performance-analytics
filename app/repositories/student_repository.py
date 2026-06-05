from sqlalchemy.orm import Session

from app.models import student
from app.models.student import Student
from app.schemas.student import StudentCreate,StudentUpdate

class StudentRepository:

    @staticmethod

    def create(db: Session , student_data:StudentCreate):
        db_student = Student(**student_data.model_dump())

        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        return db_student
    @staticmethod

    def get_all(db: Session):
        return db.query(Student).all()

    @staticmethod

    def get_by_id(db: Session , student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    @staticmethod

    def get_by_student_code(db:Session, student_code:str):

        return(
            db.query(Student).filter(Student.student_id == student_code).first()
        )

    @staticmethod
    def update(
            db: Session,
            db_student: Student,
            update_data: StudentUpdate
    ):
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(db_student, key, value)

        db.commit()
        db.refresh(db_student)

        return db_student

    @staticmethod
    def delete(db: Session, db_student: Student):
        db.delete(db_student)
        db.commit()

    @staticmethod
    def get_students_by_department(db,department: str):
        return(
            db.query(Student).filter(Student.department == department).all()

        )


