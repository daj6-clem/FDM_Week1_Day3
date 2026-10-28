import sqlite3
from data.database_manager import ConnectionManager

class ComplaintRepository:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def get_by_id(self, complaint_id):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM complaint WHERE complaint_id = ?",
                (complaint_id,)
            )

            return cursor.fetchone()
        finally:
            cursor.close()

    def get_for_customer(self, customer_id):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM complaint WHERE customer_id = ?",
                (customer_id,)
            )

            return cursor.fetchall()
        finally:
            cursor.close()

    def get_complaints(self):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM complaint",
            )

            return cursor.fetchall()
        finally:
            cursor.close

    def create(self, complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst_id):
        conn = self.connection_manager.connect()

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO COMPLAINT (
                complaint_id, 
                customer_id, 
                account_id, 
                channel, 
                category, 
                complaint_text, 
                priority, 
                status, 
                received_at,
                assigned_analyst_id
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst_id)
            )
        finally:
            cursor.close()