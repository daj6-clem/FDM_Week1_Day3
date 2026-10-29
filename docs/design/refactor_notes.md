Each repository/service/router/domain/config-dependencies should not overlap in business roles

Router: HTTP only. 
Service: business behavior and transaction use cases. 
Repository: parameterized persistence. 
Domain: entities and rules. 
Config/Dependencies: construction and environment.

Presentation - UI
Business - Core Logic/Processing Rules/Business Rules
Persistence - Data Storage and Retrieval
Database - the database

Repositories handle Data Storage and Retrieval, so they should not contain any Business code.
- Repositories and Service layer should not both have business behavior/transaction use case responsibilities
- Remove all business behavior/transaction use case code from Repositories and Add to Service Layer

MIXED RESPONSIBILITY CASES AND CODE DUPLICATION:
Before:
- Could create complaints for nonexistent customers
- Could search for complaints by nonexistent customers
- the complaint object was created and filled out in complaint_service.py

After:
- Complaints are checked for existence in complaint_service.py
- complaint object now created and filled out in complaint_repository.py layer
