-- Use CASE for unresolved 0-7, 8-30, and 31+ day groups
--	Test exact boundary dates
INSERT INTO complaint_status_history(complaint_id,old_status,new_status,changed_by,comments)
VALUES 
('CMP013',NULL,'OPEN','EMP002','Complaint registered'),
('CMP014',NULL,'OPEN','EMP002','Complaint registered');

INSERT INTO complaint(complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst_id)
VALUES
('CMP013','CUS013', 'ACC013', 'Email', 'Fee Dispute', 'Monthly fee charged incorrectly', 'High', 'OPEN', '2026-10-21 10:25:07', 'EMP002'),
('CMP014','CUS014', 'ACC014', 'Email', 'Fee Dispute', 'Monthly fee charged incorrectly', 'High', 'OPEN', '2026-10-01 10:25:07', 'EMP002');

SELECT c.complaint_id, CAST(julianday(csh.changed_at) - julianday(c.received_at) AS INTEGER) AS age_in_days,
CASE
	WHEN julianday(csh.changed_at) - julianday(c.received_at) <= 7 THEN '0-7 Days'
	WHEN julianday(csh.changed_at) - julianday(c.received_at) <= 30 THEN '8-30 Days'
	WHEN julianday(csh.changed_at) - julianday(c.received_at) >= 31 THEN '31+ Days'
END as age_group
FROM complaint as c JOIN complaint_status_history as csh
ON c.complaint_id = csh.complaint_id
WHERE status <> 'CLOSED';


-- Use a CTE to identify repeat complainants and escalation context
--	Name CTEs by business purpose
--	Keep stages readable
INSERT INTO complaint(complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst_id)
VALUES
('CMP013','CUS001', 'ACC013', 'Email', 'Fee Dispute', 'Monthly fee charged incorrectly', 'High', 'OPEN', '2026-10-21 10:25:07', 'EMP002'),
('CMP014','CUS001', 'ACC014', 'Email', 'Fee Dispute', 'Monthly fee charged incorrectly', 'High', 'OPEN', '2026-10-01 10:25:07', 'EMP002');


-- Stage 1: Identify repeat complainants
WITH repeat_complainants AS (
	SELECT complaint.customer_id, COUNT(*)
	FROM complaint
	GROUP BY complaint.customer_id
	HAVING COUNT(*) > 1
)
-- Stage 2: Join with escalation table
SELECT complaint.complaint_id, complaint.customer_id, complaint.status
FROM complaint JOIN repeat_complainants 
ON complaint.customer_id = repeat_complainants.customer_id;


-- Use ROW_NUMBER to select latest status per complaint
--	Select latest status and rank customers by complaint count
--	Explain PARTITION BY and ORDER BY

-- Step 1: rank statuses
WITH numbered_csh AS (
	SELECT complaint_id, old_status, new_status, changed_at, ROW_NUMBER() OVER (
	PARTITION BY complaint_id 
	ORDER BY changed_at DESC) as update_number
	FROM complaint_status_history
)
-- Step 2: find highest ranking statuses
SELECT complaint_id, new_status as 'latest_status', changed_at
FROM numbered_csh
WHERE update_number = 1;




-- Rank Customers by Complaint Count
-- Step 1: Count complaints
WITH cust_count AS (
	SELECT customer_id, COUNT(*) as 'no_complaints'
	FROM complaint 
	GROUP BY customer_id
)
-- Step 2: rank using ROW_NUMBER
SELECT customer_id, no_complaints, ROW_NUMBER() OVER (
	ORDER BY no_complaints DESC) 
	AS customer_rank
FROM cust_count;