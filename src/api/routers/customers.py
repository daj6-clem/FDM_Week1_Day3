from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_customer_service
from src.api.schemas import CustomerCreate
from src.services.customer_service import CustomerService

router = APIRouter()

#Added testing

@router.get("/customers/{customer_id}")
def get_by_id(customer_id:str, db:Session = Depends(get_db), service: CustomerService=Depends(get_customer_service)):
    return service.get_by_id(db, customer_id)

@router.get("/customers")
def get_customers(db:Session = Depends(get_db), service: CustomerService=Depends(get_customer_service)):
    return service.get_all(db)