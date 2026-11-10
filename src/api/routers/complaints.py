from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_complaint_service, get_customer_service
from src.api.schemas import ComplaintCreate, ComplaintResponse
from src.services.complaint_service import ComplaintService
from src.services.customer_service import CustomerService
from src.models.models import ComplaintStatus

router = APIRouter()

# added testing
## TODO: Exceptions, FastAPI

@router.get("/complaints/{complaint_id}")
def get_by_id(complaint_id:str, db:Session=Depends(get_db), service: ComplaintService = Depends(get_complaint_service)):
    return service.get_by_id(db, complaint_id)

@router.get("/complaints")
def get_complaints(db:Session=Depends(get_db), service: ComplaintService=Depends(get_complaint_service)):
    return service.get_complaints(db)

@router.get("/customers/{customer_id}/complaints")
def get_for_customer(customer_id:str, db:Session=Depends(get_db), service: ComplaintService=Depends(get_complaint_service)):
    return service.get_for_customer(db, customer_id)

@router.get("/csh")
def get_csh_history(db:Session=Depends(get_db), service: ComplaintService=Depends(get_complaint_service)):
    return service.get_csh_history(db)

@router.post("/complaints", status_code = 201)
def create_complaint(complaint:ComplaintCreate, db:Session=Depends(get_db), service: ComplaintService=Depends(get_complaint_service)):
    return service.create_complaint(db, complaint)

@router.patch("/complaints/{complaint_id}/status")
def change_status(complaint_id:str, status:ComplaintStatus, db:Session=Depends(get_db), service: ComplaintService=Depends(get_complaint_service)):
    return service.change_status(db, complaint_id, status)
