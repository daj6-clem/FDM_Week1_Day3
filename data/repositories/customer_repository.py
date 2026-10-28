from data.database_manager import ConnectionManager
import sqlite3

class CustomerRepository:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def get_by_id(self, customer_id):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM customer WHERE customer_id = ?",
                (customer_id,)
            )

            return cursor.fetchone()
        finally:
            cursor.close()

    def get_all(self):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM customer"
            )

            return cursor.fetchall()
        finally:
            cursor.close()