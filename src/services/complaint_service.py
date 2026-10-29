from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository

class ComplaintService:
    def __init__(self):
        self.complaint_repo = ComplaintRepository()
        self.customer_repo = CustomerRepository()

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
