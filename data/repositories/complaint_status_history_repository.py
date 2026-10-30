from src.models.models import Complaint, ComplaintStatus, ComplaintStatusHistory
from sqlalchemy.orm import Session
import datetime

class ComplaintStatusHistoryRepository:
    def create(self, db:Session, complaint:Complaint, old_status:ComplaintStatus, comments:str | None = None):
        csh = ComplaintStatusHistory(
            complaint_id = complaint.complaint_id,
            old_status = old_status,
            new_status = complaint.status,
            changed_by = complaint.assigned_analyst_id,
            comments = comments
        )

        db.add(csh)

        return csh

    def get_csh_history(self, db:Session):
        return db.query(ComplaintStatusHistory).all()