from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint. Performs a database query validation check
    to confirm network connection and operational database readiness.
    """
    try:
        # Perform a lightweight ping query
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "services": {
                "database": "connected"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connectivity check failed: {str(e)}"
        )
