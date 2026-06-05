# scripts/import_students.py
"""
One-time import script to load student records from an Excel sheet into PostgreSQL.
Uses pandas to read the dataset and SQLAlchemy to insert the records.
"""

import os
import sys
import pandas as pd
from sqlalchemy.orm import Session

# Add the project root directory to the python search path.
# This ensures that we can run the script directly and still import 'app'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.core.database import SessionLocal
from app.models.student import Student


def clean_val(val):
    """Helper to convert pandas NaN values to Python None."""
    if pd.isna(val):
        return None
    return val


def import_dataset(file_path: str):
    # Check if the Excel file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    print(f"Reading dataset from {file_path}...")
    try:
        # Load the Excel file. 
        # Note: The first row contains category headings like 'STUDENT INFORMATION'.
        # We use header=1 to make the second row (containing actual column headers) the header.
        df = pd.read_excel(file_path, header=1)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    total_rows = len(df)
    imported_rows = 0
    skipped_rows = 0
    failed_rows = 0

    print(f"Total records found in Excel: {total_rows}")
    print("Connecting to database...")

    # Create a single database session
    db: Session = SessionLocal()

    try:
        # Fetch existing student IDs from the database to avoid importing duplicates.
        print("Fetching existing student IDs from database...")
        existing_student_ids = {s[0] for s in db.query(Student.student_id).all()}
        print(f"Found {len(existing_student_ids)} existing students in database.")

        # Keep track of student IDs we process in this run to skip duplicates within the Excel itself.
        seen_in_batch = set()

        print("Starting import process...")
        for index, row in df.iterrows():
            row_num = index + 3  # Excel row number (1-based, plus header rows)

            # 1. Read values from the row and clean NaN values
            student_id = clean_val(row.get("Student ID"))
            full_name = clean_val(row.get("Full Name"))
            department = clean_val(row.get("Department"))
            semester = clean_val(row.get("Semester"))
            cgpa = clean_val(row.get("CGPA"))
            internal_marks = clean_val(row.get("Internal Marks"))
            exam_score = clean_val(row.get("Exam Score"))
            backlogs_count = clean_val(row.get("Backlogs Count"))
            assignments_completed = clean_val(row.get("Assignments Completed"))
            attendance_percentage = clean_val(row.get("Attendance %"))
            library_visits = clean_val(row.get("Library Visits"))
            workshop_attendance = clean_val(row.get("Workshop Attendance"))

            # 2. Validate required fields
            if not student_id or not full_name or not department or semester is None:
                print(f"Row {row_num}: Failed - Missing required fields (Student ID, Full Name, Department, or Semester)")
                failed_rows += 1
                continue

            # Clean/strip string fields
            student_id = str(student_id).strip()
            full_name = str(full_name).strip()
            department = str(department).strip()

            # 3. Check for duplicates (in DB or current batch)
            if student_id in existing_student_ids or student_id in seen_in_batch:
                # Silently skip duplicates
                skipped_rows += 1
                continue

            # 4. Data validation and type safety
            try:
                # Convert numeric fields and validate ranges
                semester = int(semester)
                if not (1 <= semester <= 8):
                    raise ValueError(f"Semester must be between 1 and 8, got {semester}")

                if cgpa is not None:
                    cgpa = float(cgpa)
                    if not (0.0 <= cgpa <= 10.0):
                        raise ValueError(f"CGPA must be between 0.0 and 10.0, got {cgpa}")

                if internal_marks is not None:
                    internal_marks = int(internal_marks)
                    if not (0 <= internal_marks <= 100):
                        raise ValueError(f"Internal Marks must be between 0 and 100, got {internal_marks}")

                if exam_score is not None:
                    exam_score = int(exam_score)
                    if not (0 <= exam_score <= 100):
                        raise ValueError(f"Exam Score must be between 0 and 100, got {exam_score}")

                if backlogs_count is not None:
                    backlogs_count = int(backlogs_count)
                    if backlogs_count < 0:
                        raise ValueError(f"Backlogs Count cannot be negative, got {backlogs_count}")

                if attendance_percentage is not None:
                    attendance_percentage = float(attendance_percentage)
                    if not (0.0 <= attendance_percentage <= 100.0):
                        raise ValueError(f"Attendance % must be between 0.0 and 100.0, got {attendance_percentage}")

                if assignments_completed is not None:
                    assignments_completed = int(assignments_completed)
                    if assignments_completed < 0:
                        raise ValueError(f"Assignments Completed cannot be negative, got {assignments_completed}")

                if library_visits is not None:
                    library_visits = int(library_visits)
                    if library_visits < 0:
                        raise ValueError(f"Library Visits cannot be negative, got {library_visits}")

                if workshop_attendance is not None:
                    workshop_attendance = int(workshop_attendance)
                    if workshop_attendance < 0:
                        raise ValueError(f"Workshop Attendance cannot be negative, got {workshop_attendance}")

            except Exception as val_error:
                print(f"Row {row_num} (Student: {student_id}): Failed validation - {val_error}")
                failed_rows += 1
                continue

            # 5. Create student ORM model instance
            student = Student(
                student_id=student_id,
                full_name=full_name,
                department=department,
                semester=semester,
                cgpa=cgpa,
                internal_marks=internal_marks,
                exam_score=exam_score,
                backlogs_count=backlogs_count,
                attendance_percentage=attendance_percentage,
                assignments_completed=assignments_completed,
                library_visits=library_visits,
                workshop_attendance=workshop_attendance,
            )

            # 6. Add to session
            db.add(student)
            seen_in_batch.add(student_id)
            imported_rows += 1

        # 7. Commit transaction to the database
        print("Committing transaction...")
        db.commit()
        print("Import completed successfully!")

    except Exception as db_error:
        print(f"Database transaction error: {db_error}")
        print("Rolling back transaction...")
        db.rollback()
        # Reset counters since the transaction failed
        imported_rows = 0
        skipped_rows = 0
        failed_rows = total_rows
    finally:
        db.close()

    # Print summary of execution
    print("\n------------------------------")
    print(f"Total Rows: {total_rows}")
    print(f"Imported Rows: {imported_rows}")
    print(f"Skipped Rows: {skipped_rows}")
    print(f"Failed Rows: {failed_rows}")
    print("------------------------------")

    # Run verification queries directly to verify import
    verify_import()


def verify_import():
    """Verify that records were successfully imported."""
    print("\n--- Verification Section ---")
    db: Session = SessionLocal()
    try:
        count = db.query(Student).count()
        print(f"Total students currently in database: {count}")
        
        # Display the first few records
        first_students = db.query(Student).order_by(Student.id).limit(3).all()
        print("\nFirst few imported records:")
        for idx, student in enumerate(first_students, 1):
            print(
                f"{idx}. ID: {student.student_id} | Name: {student.full_name} | "
                f"Dept: {student.department} | Semester: {student.semester} | CGPA: {student.cgpa}"
            )
        
        if count > 0:
            print("\nVerification status: SUCCESS")
        else:
            print("\nVerification status: FAILED (No records found)")
    except Exception as e:
        print(f"Verification error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    dataset_file = "student_analytics_dataset.xlsx"
    import_dataset(dataset_file)
