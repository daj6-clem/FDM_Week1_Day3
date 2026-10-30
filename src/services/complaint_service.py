from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository
from data.repositories.complaint_status_history_repository import ComplaintStatusHistoryRepository
from src.models.models import ComplaintStatus, Complaint
from fastapi import HTTPException

class ComplaintService:
    def __init__(self):
        self.complaint_repo = ComplaintRepository()
        self.customer_repo = CustomerRepository()
        self.csh_repo = ComplaintStatusHistoryRepository()

    def get_by_id(self, db, complaint_id):
        return self.complaint_repo.get_by_id(db, complaint_id)
    
    def get_complaints(self, db):
        return self.complaint_repo.get_complaints(db)
    
    def get_for_customer(self, db, customer_id):
        customer = self.customer_repo.get_by_id(db, customer_id)

        if customer is None:
            raise ValueError("Cannot get complaint: customer does not exist.")
        
        return self.complaint_repo.get_for_customer(db, customer_id)

    def create_complaint(self, db, complaint):
        customer = self.customer_repo.get_by_id(db, complaint.customer_id)
        if customer is None:
            raise ValueError("Cannot create complaint: customer does not exist.")

        complaint_id = self.complaint_repo.generate_complaint_id(db)
        
        return self.complaint_repo.create(db, complaint, complaint_id)

    def change_status(self, db, complaint_id: str, status:ComplaintStatus):
        complaint = self.complaint_repo.get_by_id(db, complaint_id)

        if complaint is None:
            raise HTTPException(status_code = 404, detail = f"No complaint with id complaint_id = {complaint_id}.")
        
        try:
            old_status = complaint.status
            complaint.change_status(status)

            self.csh_repo.create(db, complaint, old_status)
            db.commit()
            db.refresh(complaint)
        except ValueError as e:
            db.rollback()
            raise HTTPException(status_code = 409, detail = str(e))

        return complaint

    def get_csh_history(self, db):
        return self.csh_repo.get_csh_history(db)