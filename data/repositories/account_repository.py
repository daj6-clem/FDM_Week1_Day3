from models.models import Account

class AccountRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_for_customer(self, customer_id):
        with self.session_factory() as session:
            return (session.query(Account)
                    .filter(Account.customer_id == customer_id)
                    .first())

    def get_all(self):
        with self.session_factory() as session:
            return (session.query(Account).all())
