from src.models.models import Complaint, ComplaintStatus
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

    def generate_complaint_id(self, db):
        latest = (
            db.query(Complaint)
            .order_by(Complaint.complaint_id.desc())
            .first()
        )
        if latest is None:
            return "CMP001"

        num = int(latest.complaint_id[3:])
        return f"CMP{num+1:03d}"

    def create(self, db:Session, complaint_data, complaint_id):
        complaint = Complaint(
            complaint_id = complaint_id,
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
        db.refresh(complaint)

        return complaint

    def save_complaint(self, db:Session, complaint:Complaint):

        db.commit()
        db.refresh(complaint)

        return complaint