from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)
from app.services.student import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    """Create a new student record."""
    try:
        return StudentService.create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    """Return all student records."""
    return StudentService.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    """Return a single student by their numeric database ID."""
    try:
        return StudentService.get_student(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    update_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing student record (partial update supported)."""
    try:
        return StudentService.update_student(db, student_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    """Delete a student record by their numeric database ID."""
    try:
        return StudentService.delete_student(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
