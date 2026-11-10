from abc import ABC, abstractmethod
from src.models.models import Complaint
from sqlalchemy.orm import Session

class ComplaintRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, db:Session, complaint_id):
        pass

    @abstractmethod
    def get_for_customer(self, db:Session, customer_id):
        pass

    @abstractmethod
    def get_complaints(self, db:Session):
        pass

    @abstractmethod
    def generate_complaint_id(self, db):
        pass

    @abstractmethod
    def create(self, db:Session, complaint_data, complaint_id):
        pass

    @abstractmethod
    def save_complaint(self, db:Session, complaint:Complaint):
        pass