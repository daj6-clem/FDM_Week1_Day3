from dotenv import load_dotenv
import sqlite3
import os

## BUILD CONNECTION MANAGER
# Load environment settings and manage lifecycle
# Open/close safely
# commit/rollback correctly
# Do not expose credentials

load_dotenv()

db_path = os.getenv("DB_PATH")

class ConnectionManager:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH")
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()
