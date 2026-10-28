import sqlite3
from data.database_manager import ConnectionManager

class AccountRepository:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def get_for_customer(self, customer_id):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM account WHERE customer_id = ?",
                (customer_id,)
            )

            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all(self):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM account"
            )

            return cursor.fetchall()
        finally:
            cursor.close()
