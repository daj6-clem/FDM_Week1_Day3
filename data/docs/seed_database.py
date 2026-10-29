from database_manager import ConnectionManager
import sqlite3

# INITIALIZATION
# Connect to database
# Read and execute database_schema.sql
# Create all tables
def initialize_database(conn):
    print("Initializing...")
    cursor = conn.cursor()
    try:
        with open("data/database_schema.sql") as f:
            cursor.executescript(f.read())
    finally:
        cursor.close()

# SEEDING
def seed_database(conn):
    cursor = conn.cursor()
    try:
        with open("data/seeddatacrs.sql") as f2:
            cursor.executescript(f2.read())

        with open("data/dataseedingExtended.sql") as f:
            cursor.executescript(f.read())
    finally:
        cursor.close()

def drop_tables(conn):
    print("Dropping tables...")
    cursor = conn.cursor()
    try:
        with open("data/dropScriptBankCRS.sql") as f:
            cursor.executescript(f.read())
    finally:
        cursor.close()

# Connect to database
# Create a cursor
# Pass cursor to two functions
# Commit changes
# Close cursor
# Close connection
def main():
    connection_manager = ConnectionManager()
    conn = connection_manager.connect()

    try:
        drop_tables(conn)
        initialize_database(conn)
        seed_database(conn)

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


main()