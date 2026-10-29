from data.repositories.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def get_by_id(self, db, customer_id):
        return self.repository.get_by_id(db, customer_id)

    def get_all(self, db):
        return self.repository.get_all(db)