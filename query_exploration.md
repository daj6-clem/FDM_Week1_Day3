Inspect Tables, Counts, Data Types, and Null Patterns:

All sample accounts are active
Account types are Chequing, Savings, and Business
Primary Account Keys start with ACC, it is a text field

Audit Log uses 'performed by' alias for emp_id
Audit logs can be complaints, service requests, investigations, recommendations, review requests, or customer responses
Each entity has an id
Audit logs record actions on entities, employee ids, timestamps, and details
Integer PK

Complaint uses assigned_analyst_id as an alias for emp_id

complaint_status_history has nulls for old_status (all are when the new status is open, so this is their first entry)
integer primary key, other fields are all text

customer has only text fields, including phone number
Customer segment can be retail, premier, business

customer_response has text primary key
The response_text has 10 pre-filled responses for different purposes
Also has a send date

employee has all text fields, empid, name, email, and role
Roles are analyst, reviewer, manager, supervisor

fee has null fields for transaction_id, but they're for maintenance and wires
fee has a reversed_flag integer
Fee types are overdraft, maintenance, wire, business service, card replacement

investigation has null fields for completed_at, assuming those aren't finished
also has investigation_summary

policy_document has names, version number, effective date, and status

policy_section has titles and text

recommendation has text, confidence score, a generation date, and the relevant ids

review_decision has the decision on the recommendation, the reasons, and the date

review_request has timestamps and statuses for recommendations and reviewers for complaints

service_request has request types, status, creation dates, and closed dates
Some closed dates are NULL (still open)

transactions has transaction type, amount, date, balance before and after, and a description for what the transaction is