from models.models import Account
from sqlalchemy.orm import Session

class AccountRepository:
    def get_for_customer(self, db:Session, customer_id):
        return (db.query(Account)
                .filter(Account.customer_id == customer_id)
                .all()
        )

    def get_all(self, db:Session):
        return (db.query(Account).all())
