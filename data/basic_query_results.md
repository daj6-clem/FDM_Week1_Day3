# Basic Query Questions

1. List all open complaints.
CMP001, CMP004, CMP006, CMP008, CMP010
2. List high-priority unresolved complaints.
CMP001, CMP003, CMP006, CMP007
3. Count complaints by status.
1 Closed, 2 In progress, 5 open, 2 under review
4. Count complaints by category.
1 Card Issue, 1 customer service, 3 fee dispute, 1 fraud claim, 1 online banking, 1 service delay, 2 transaction error
5. Show complaints for a supplied customer ID.
CUS005 only has CMP005
6. Show complaints opened within a supplied date range.
CMP001, CMP002, CMP003, CMP004, CMP005, and CMP006 were opened between 2025-01-01 and 2025-01-20
7. List closed complaints where date\_closed is missing (expected zero).
This one was hard to understand but I think it wants CMP002, CMP003, CMP005, CMP007, CMP008, and CMP009.
8. Show the ten most recently opened complaints.
On the given data set, this yields CMP001-10 because there are only 10 complaints.

