from sqlalchemy.orm import Session
from src.models.models import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_account_id(self, account_id):
        return (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.processed_at.desc())
            .all()
        )

    def get_deposits(self, account_id):
        return (
            self.db.query(Transaction)
            .filter(
                Transaction.account_id == account_id,
                Transaction.description == "DEPOSIT"
            )
            .order_by(Transaction.processed_at.desc())
            .all()
        )