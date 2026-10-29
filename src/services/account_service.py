from data.repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self):
        self.repository = AccountRepository()

    def get_for_customer(self, db, customer_id):
        return self.repository.get_by_id(db, customer_id)

    def get_all(self, db):
        return self.repository.get_all(db)