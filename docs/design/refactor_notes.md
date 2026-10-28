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
- Customer_Repository.py rolls back in its create() function in the event of an exception
- Business rules mixed and duplicated between models and service layer
- Duplication - Don't need to check that something is not None and not an empty string and not within its enumerated type

After:
- Repositories lose rollbacks and commits, those go to service layer, Repositories keep the SQL
- Business rules constrained to a single object or entity are moved to models, business rules involving workflow that reference multiple entities are moved to service layer
    - Checking for enumerated types should be in models
    - Checking to see if a customer exists for complaint creation should be in service
- Removed redundant checks
