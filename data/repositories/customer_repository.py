from src.models.models import Customer
from sqlalchemy.orm import Session

class CustomerRepository:
    def get_by_id(self, db:Session, customer_id):
        return (db.query(Customer)
                .filter(Customer.customer_id == customer_id)
                .first()
        )

    def get_all(self, db:Session):
        return (db.query(Customer).all())