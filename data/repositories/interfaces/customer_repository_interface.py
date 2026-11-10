from src.models.models import Customer
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class CustomerRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, db:Session, customer_id):
        pass
         

    @abstractmethod
    def get_all(self, db:Session):
        pass