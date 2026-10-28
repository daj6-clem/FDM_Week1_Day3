from src.models.models import Customer

class CustomerRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_by_id(self, customer_id):
        with self.session_factory() as session:
            return (
                session.query(Customer)
                .filter(Customer.customer_id == customer_id)
                .first()
            )

    def get_all(self):
        with self.session_factory() as session:
            return (
                session.query(Customer).all()
            )