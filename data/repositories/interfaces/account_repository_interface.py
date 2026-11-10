from src.models.models import Account
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class AccountRepositoryInterface(ABC):
    @abstractmethod
    def get_for_customer(self, db:Session, customer_id):
        pass

    @abstractmethod
    def get_all(self, db:Session):
        pass
