from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.api.schemas import ComplaintCreate
from src.services.complaint_service import ComplaintService

service = ComplaintService()

router = APIRouter()


## TODO: Exceptions, FastAPI

@router.get("/complaints/{complaint_id}")
def get_by_id(complaint_id, db:Session=Depends(get_db)):
    return service.get_by_id(db, complaint_id)

@router.get("/complaints")
def get_complaints(db:Session=Depends(get_db)):
    return service.get_complaints(db)

@router.get("/complaints/customers/{customer_id}")
def get_for_customer(customer_id:str, db:Session=Depends(get_db)):
    return service.get_for_customer(db, customer_id)

@router.post("/complaints")
def create_complaint(complaint:ComplaintCreate, db:Session = Depends(get_db)):
    print("post hit.")
    return service.create_complaint(db, complaint)