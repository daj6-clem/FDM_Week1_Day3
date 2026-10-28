from models.models import Complaint

# SERVICES INTERFACE DIRECTLY WITH REPOSITORIES
# THEY WILL CALL THE METHODS IN THE REPOSITORY
# BUT ALSO APPLY BUSINESS BEHAVIOR AND TRANSACTION USE CASES
# IF a business rule is self contained to one entity, it goes in the model
# IF a buesiness rule references multiple entities, it stays in service layer

class ComplaintService:
    # injecting dependencies: we need to be able to plug fake complaint repositories into this
    def __init__(self, session_factory, complaint_repo, customer_repo):
        self.session_factory = session_factory
        self.complaint_repo = complaint_repo
        self.customer_repo = customer_repo

    def get_by_id(self, complaint_id):
        return self.complaint_repo.get_by_id(complaint_id)
    
    def get_complaints(self):
        return self.complaint_repo.get_complaints()
    
    def get_for_customer(self, customer_id):
        customer = self.customer_repo.get_by_id(customer_id)

        if customer is None:
            raise ValueError("Cannot get complaint: customer does not exist.")
        
        return self.complaint_repo.get_for_customer(customer_id)

    def create_complaint(self, complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst_id):
        customer = self.customer_repo.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Cannot create complaint: customer does not exist.")
        with self.session_factory() as session:
            try:
                complaint = Complaint(
                    complaint_id = complaint_id,
                    customer_id = customer_id,
                    account_id = account_id,
                    channel = channel,
                    category = category,
                    complaint_text = complaint_text,
                    priority = priority,
                    status = status,
                    received_at = received_at,
                    assigned_analyst_id = assigned_analyst_id
                )

                self.complaint_repo.create(
                    session, complaint
                )
                session.commit()
                return complaint
            except Exception:
                session.rollback()
                raise
