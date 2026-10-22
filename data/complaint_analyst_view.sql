CREATE VIEW complaint_analyst_view AS
SELECT complaint.complaint_id, complaint.customer_id, complaint.account_id, category, complaint_text, priority, complaint.status, received_at, account.account_number, account.account_type, account.current_balance 
FROM complaint as co
LEFT JOIN account on co.customer_id = account.customer_id;