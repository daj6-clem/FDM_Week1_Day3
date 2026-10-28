CUSTOMER: ID, first name, last name, email, phone, segment, date created

Enums:

&#x09;Segment (Retail, Premier, Business)



Phone number can't be more than 10 digits

ID must be CUS###

No Transition Rules





ACCOUNT: Account ID, Customer ID, Account Number, Account Type, Status, Current Balance, opened date

Enums:

&#x09;Account Type (Checking, Savings, Business)

&#x09;Status (Active, Inactive)

ID must be ACC###

Valid transitions: Active -> Inactive, Inactive -> Active





COMPLAINT: Complaint ID, Customer ID, Account ID, Channel, Category, Complaint Text, Priority, Status, Received At, Assigned Analyst

Enums:

&#x09;Status (Open, In Progress, Under Review, Closed)

&#x09;Channel (Phone, Email, Branch, Web)

&#x09;Priority (High, Medium, Low, Critical)

&#x09;Category (Fee Dispute, Service Delay, Card Issue, Customer Service, Transaction Error, Online Banking, Fraud Claim)

ID must be CMP###

Valid Transitions:

&#x09;OPEN -> IN\_PROGRESS

&#x09;IN\_PROGRESS -> UNDER\_REVIEW

&#x09;IN\_PROGRESS -> CLOSED

&#x09;UNDER\_REVIEW -> CLOSED





COMPLAINT STATUS HISTORY: History ID, complaint ID, old\_status, new\_status, changed\_by, changed\_at, comments

Enums:

&#x09;old\_status (NULL, Open, In Progress, Under Review, Closed)

&#x09;New\_status (Open, In Progress, Under Review, Closed)

VALID Transitions: None (We create new entries instead of transitioning existing rows)



ID must be #

