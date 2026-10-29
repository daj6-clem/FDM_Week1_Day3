from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.dependencies import get_db

router = APIRouter()
# Request urls go to router which maps it to the below function and returns the given response
@router.get("/health/live")
def live():
    return {"status":"alive"}

@router.get("/health/ready")
def ready(db:Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected"
        }

    except Exception:
        raise HTTPException(
            status_code = 503,
            detail = "Database unavailable"
        )