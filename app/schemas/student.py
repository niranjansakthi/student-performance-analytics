from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class StudentCreate(BaseModel):
    student_id: str
    full_name: str
    department: str
    semester: int
    cgpa: Optional[float] = None
    internal_marks: Optional[int] = None
    exam_score: Optional[int] = None
    backlogs_count: Optional[int] = 0
    attendance_percentage: Optional[float] = None
    assignments_completed: Optional[int] = 0
    library_visits: Optional[int] = 0
    workshop_attendance: Optional[int] = 0

class StudentUpdate(BaseModel):
    semester: Optional[int] = None
    cgpa: Optional[float] = None
    internal_marks: Optional[int] = None
    exam_score: Optional[int] = None
    backlogs_count: Optional[int] = None
    attendance_percentage: Optional[float] = None
    assignments_completed: Optional[int] = None
    library_visits: Optional[int] = None
    workshop_attendance: Optional[int] = None

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: str
    full_name: str
    department: str
    semester: int
    cgpa: Optional[float]
    internal_marks: Optional[int]
    exam_score: Optional[int]
    backlogs_count: Optional[int]
    attendance_percentage: Optional[float]
    assignments_completed: Optional[int]
    library_visits: Optional[int]
    workshop_attendance: Optional[int]
    created_at: datetime