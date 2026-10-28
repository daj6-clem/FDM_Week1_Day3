from models.models import Complaint

class ComplaintRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_by_id(self, complaint_id):
        with self.session_factory() as session:
            return (session.query(Complaint)
                    .filter(Complaint.complaint_id == complaint_id)
                    .first()
            )

    def get_for_customer(self, customer_id):
        with self.session_factory() as session:
            return (session.query(Complaint)
                    .filter(Complaint.customer_id == customer_id)
                    .all()
            )

    def get_complaints(self):
        with self.session_factory() as session:
            return (session.query(Complaint).all())

    def create(self, session, complaint):
        session.add(complaint)
        
        return complaint