from data.connection import SessionLocal
from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository
from data.repositories.account_repository import AccountRepository
from data.repositories.complaint_status_history_repository import ComplaintStatusHistoryRepository
from src.services.complaint_service import ComplaintService
from src.services.customer_service import CustomerService
from src.services.account_service import AccountService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_complaint_service():
    complaint_repo = ComplaintRepository()
    customer_repo = CustomerRepository()
    csh_repo = ComplaintStatusHistoryRepository()

    return ComplaintService(
        complaint_repo = complaint_repo,
        customer_repo = customer_repo,
        csh_repo = csh_repo
    )

def get_customer_service():
    repository = CustomerRepository()
    return CustomerService(repository = repository)

def get_account_service():
    repository = AccountRepository()
    return AccountService(repository = repository)