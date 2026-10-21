--JOIN QUERY QUESTIONS
-- Show each complaint with customer name.
SELECT customer.first_name, customer.last_name, complaint.complaint_text from customer 
INNER JOIN complaint 
on customer.customer_id = complaint.customer_id



-- Add optional account type without dropping complaints that have no account.
SELECT c.first_name, c.last_name, co.complaint_text, a.account_type from customer as c
INNER JOIN complaint as co on c.customer_id = co.customer_id
LEFT JOIN account as a on c.customer_id = a.customer_id;



-- Verify distinct complaint count before and after joins.
SELECT COUNT(*) FROM customer INNER JOIN complaint on customer.customer_id = complaint.customer_id
LEFT JOIN account as a on customer.customer_id = a.customer_id;
SELECT COUNT(DISTINCT complaint_id) 
FROM customer INNER JOIN complaint on customer.customer_id = complaint.customer_id
LEFT JOIN account as a on customer.customer_id = a.customer_id;