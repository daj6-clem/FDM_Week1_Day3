from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.api.schemas import CustomerCreate
from src.services.customer_service import CustomerService

service = CustomerService()

router = APIRouter()

@router.get("/customers/{customer_id}")
def get_by_id(customer_id:str, db:Session = Depends(get_db)):
    customer = service.get_by_id(db, customer_id)

    if customer:
        return customer
    else:
        raise HTTPException(status_code = 404, detail = f"No customer with id = {customer_id}.")

@router.get("/customers")
def get_customers(db:Session = Depends(get_db)):
    return service.get_all(db)