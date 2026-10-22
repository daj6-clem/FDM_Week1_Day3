SELECT COUNT(\*) FROM complaint; -> Yields 10



SELECT COUNT(\*) FROM customer INNER JOIN complaint on customer.customer\_id = complaint.customer\_id

LEFT JOIN account as a on customer.customer\_id = a.customer\_id; -> Yields 10



SELECT COUNT(DISTINCT complaint\_id) 

FROM customer INNER JOIN complaint

ON customer.customer\_id = complaint.customer\_id

LEFT JOIN account as a

ON customer.customer\_id = a.customer\_id; -> Yields 10





Explain one-to-many duplication:

One record in a parent table, like customer, could be linked to multiple records in a child table, like account or complaint, so when you do a join the account or complaint tables may contain repeated or duplicated information from the parent table's primary key showing up multiple times as a foreign key.

