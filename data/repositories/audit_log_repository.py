from sqlalchemy.orm import Session
from src.models.models import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, log: AuditLog):
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log