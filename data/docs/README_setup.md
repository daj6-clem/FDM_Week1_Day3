Prerequisites:
    - Need an existing database file, in this case Banking_Complaint_Assistant.db
    - Need data/database_schema.sql file
    - Need data/dataseedingExtended.sql
    - Need data/seeddatacrs.sql
    - Need data/database_manager.py

Command:
    - Only need to run seed_database.py with the requisite files
    - All functions will be run from main

Expected output:
    - The program will run the database seeding SQL scripts to create tables and populate the database

Troubleshooting:
    - Main is wrapped in a try except so any failures should be displayed as exceptions.
    - The system was originally intended to use .csv files but the supplied csv files do not match the database requirements we were given
    - The database seeding files are necessary
    - The database name is Banking_Complaint_Assistant.db