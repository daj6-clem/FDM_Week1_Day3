from data.repositories.customer_repository import CustomerRepository
from src.api.error_handlers.error_handlers import CustomerNotFoundException
from data.repositories.interfaces.customer_repository_interface import CustomerRepositoryInterface

class CustomerService:
    def __init__(self, repository:CustomerRepositoryInterface):
        self.repository = repository

    def get_by_id(self, db, customer_id):
        customer = self.repository.get_by_id(db, customer_id)

        if customer is None:
            raise CustomerNotFoundException(
                f"No customer with id {customer_id}."
            )

        return customer

    def get_all(self, db):
        return self.repository.get_all(db)