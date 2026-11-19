from sqlalchemy.orm import Session
from src.models.models import Fee


class FeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_account_id(self, account_id):
        return (
            self.db.query(Fee)
            .filter(Fee.account_id == account_id)
            .order_by(Fee.charged_at.desc())
            .all()
        )

    def get_active_fees(self, account_id: str):
        return (
            self.db.query(Fee)
            .filter(
                Fee.account_id == account_id,
                Fee.reversed_flag == 0
            )
            .order_by(Fee.charged_at.desc())
            .all()
        )