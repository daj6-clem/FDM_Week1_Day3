from src.models.models import Complaint
from sqlalchemy.orm import Session

class ComplaintRepository:
    def get_by_id(self, db:Session, complaint_id):
        return (db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
        )

    def get_for_customer(self, db:Session, customer_id):
        return (db.query(Complaint)
                .filter(Complaint.customer_id == customer_id)
                .all()
        )

    def get_complaints(self, db:Session):
        return db.query(Complaint).all()

    def create(self, db:Session, complaint_data):
        complaint = Complaint(
            complaint_id = complaint_data.complaint_id,
            customer_id = complaint_data.customer_id,
            account_id = complaint_data.account_id,
            channel = complaint_data.channel,
            category = complaint_data.category,
            complaint_text = complaint_data.complaint_text,
            priority = complaint_data.priority,
            status = complaint_data.status,
            received_at = complaint_data.received_at,
            assigned_analyst_id = complaint_data.assigned_analyst_id
        )

        db.add(complaint)
        db.commit()
        db.refresh()

        return complaint