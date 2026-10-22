-- Complaint Volume by status, category, and month
SELECT status, COUNT(*) FROM complaint GROUP BY status;
SELECT category , COUNT(*) FROM complaint GROUP BY category;
SELECT strftime('%Y-%m', received_at) as complaint_month, COUNT(*) as complaint_count 
FROM complaint 
GROUP BY strftime('%Y-%m', received_at)
ORDER BY complaint_month;


-- Open and escalated backlog
SELECT COUNT(*) FROM complaint WHERE status="OPEN" OR status = "UNDER_REVIEW";


-- Distinct affected customers
SELECT COUNT(DISTINCT customer_id) FROM complaint;

-- average closed-case resolution days by category
SELECT complaint.category, AVG(julianday(complaint_status_history.changed_at) - julianday(complaint.received_at))
FROM complaint LEFT JOIN complaint_status_history
ON complaint.complaint_id = complaint_status_history.complaint_id
WHERE complaint.status = "CLOSED"
GROUP BY category;

