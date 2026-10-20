--BASIC QUERY QUESTIONS--

--	List all open complaints.
SELECT complaint_id FROM complaint
WHERE status = "OPEN";


--	List high-priority unresolved complaints.
SELECT complaint_id FROM complaint
WHERE status IS NOT "CLOSED" 
AND priority = "High";


--	Count complaints by status.
SELECT status, COUNT(*) FROM complaint
GROUP BY status;


--	Count complaints by category.
SELECT category, COUNT(*) FROM complaint
GROUP BY category;


--	Show complaints for a supplied customer ID.
SELECT complaint_id FROM complaint
WHERE customer_id = ?;


--	Show complaints opened within a supplied date range.
SELECT complaint_id FROM complaint
WHERE received_at BETWEEN ? AND ?;


--	List closed complaints where date_closed is missing (expected zero).
SELECT complaint_id FROM complaint
LEFT JOIN service_request ON complaint.customer_id = service_request.customer_id
WHERE closed_at IS NULL;


--	Show the ten most recently opened complaints.
SELECT complaint_id FROM complaint
ORDER BY received_at asc
LIMIT 10;



