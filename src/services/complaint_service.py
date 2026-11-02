from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository
from data.repositories.complaint_status_history_repository import ComplaintStatusHistoryRepository
from src.models.models import ComplaintStatus, Complaint
from fastapi import HTTPException
from src.api.error_handlers.error_handlers import CustomerNotFoundException, ComplaintNotFoundException, InvalidStatusTransitionException

# Note: Added tests

class ComplaintService:
    def __init__(self):
        self.complaint_repo = ComplaintRepository()
        self.customer_repo = CustomerRepository()
        self.csh_repo = ComplaintStatusHistoryRepository()

    def get_by_id(self, db, complaint_id):
        complaint = self.complaint_repo.get_by_id(db, complaint_id)

        if complaint is None:
            raise ComplaintNotFoundException(
                f"No complaint with id {complaint_id}."
            )

        return complaint
    
    def get_complaints(self, db):
        return self.complaint_repo.get_complaints(db)
    
    def get_for_customer(self, db, customer_id):
        customer = self.customer_repo.get_by_id(db, customer_id)

        if customer is None:
            raise CustomerNotFoundException("Cannot get complaint: customer does not exist.")
        
        return self.complaint_repo.get_for_customer(db, customer_id)

    def create_complaint(self, db, complaint):
        customer = self.customer_repo.get_by_id(db, complaint.customer_id)
        if customer is None:
            raise CustomerNotFoundException("Cannot create complaint: customer does not exist.")

        complaint_id = self.complaint_repo.generate_complaint_id(db)

        try:
            complaint = self.complaint_repo.create(db, complaint, complaint_id)
            # Boundary note - Complaint and Initial Status event form one transaction.
            # Above is the complaint. Below is the initial status event.
            
            self.csh_repo.create(db, complaint, None)
        
            db.commit()
            db.refresh(complaint)

            return complaint
        except:
            db.rollback()
            raise 

    def change_status(self, db, complaint_id: str, status:ComplaintStatus):
        complaint = self.complaint_repo.get_by_id(db, complaint_id)

        if complaint is None:
            raise ComplaintNotFoundException(f"No complaint with id complaint_id = {complaint_id}.")
        
        try:
            old_status = complaint.status
            complaint.change_status(status)

            self.csh_repo.create(db, complaint, old_status)
            db.commit()
            db.refresh(complaint)
        except ValueError as e:
            db.rollback()
            raise InvalidStatusTransitionException(str(e))

        return complaint

    def get_csh_history(self, db):
        return self.csh_repo.get_csh_history(db)