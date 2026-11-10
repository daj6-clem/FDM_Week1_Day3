from src.models.models import Complaint, ComplaintStatus, ComplaintStatusHistory
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class ComplaintStatusHistoryRepositoryInterface(ABC):
    @abstractmethod
    def create(self, db:Session, complaint:Complaint, old_status:ComplaintStatus, comments:str | None = None):
        pass

    @abstractmethod
    def get_csh_history(self, db:Session):
        pass