-- =====================================================
-- ADDITIONAL COMPLAINTS (CMP011 - CMP030)
-- =====================================================

INSERT INTO complaint VALUES

-- CUS001 (3 additional complaints)
('CMP011','CUS001','ACC001','Web','Service Delay',
 'Complaint not updated within SLA',
 'Medium','OPEN','2025-02-01 09:15:00','EMP001'),

('CMP012','CUS001','ACC001','Phone','Fee Dispute',
 'Unexpected service charge',
 'High','UNDER_REVIEW','2025-02-03 10:00:00','EMP002'),

('CMP013','CUS001','ACC001','Email','Customer Service',
 'Unsatisfactory support response',
 'Low','OPEN','2025-02-05 14:00:00','EMP006'),

-- CUS002 (2 additional complaints)
('CMP014','CUS002','ACC002','Web','Online Banking',
 'Mobile app login issue',
 'Medium','OPEN','2025-02-06 09:30:00','EMP006'),

('CMP015','CUS002','ACC002','Phone','Transaction Error',
 'Duplicate debit posted',
 'High','IN_PROGRESS','2025-02-08 11:15:00','EMP001'),

-- CUS003 (3 additional complaints)
('CMP016','CUS003','ACC003','Branch','Transaction Error',
 'ATM withdrawal discrepancy',
 'High','UNDER_REVIEW','2025-02-09 13:10:00','EMP001'),

('CMP017','CUS003','ACC003','Email','Fee Dispute',
 'Wire fee charged incorrectly',
 'Medium','OPEN','2025-02-11 09:40:00','EMP002'),

('CMP018','CUS003','ACC003','Web','Service Delay',
 'No response received',
 'Low','OPEN','2025-02-12 16:00:00','EMP006'),

-- CUS004 (1 additional complaint)
('CMP019','CUS004','ACC004','Phone','Customer Service',
 'Long hold times',
 'Low','OPEN','2025-02-13 10:45:00','EMP007'),

-- CUS005 (2 additional complaints)
('CMP020','CUS005','ACC005','Email','Fee Dispute',
 'Business account charge disputed',
 'Medium','OPEN','2025-02-14 11:00:00','EMP002'),

('CMP021','CUS005','ACC005','Branch','Service Delay',
 'Delayed account update',
 'Medium','IN_PROGRESS','2025-02-15 15:00:00','EMP001'),

-- CUS006 (2 additional complaints, one NULL account)
('CMP022','CUS006','ACC006','Web','Card Issue',
 'Card declined during purchase',
 'High','OPEN','2025-02-16 09:00:00','EMP002'),

('CMP023','CUS006',NULL,'Phone','Customer Service',
 'General complaint regarding service',
 'Low','OPEN','2025-02-17 14:30:00','EMP006'),

-- CUS007 (3 additional complaints)
('CMP024','CUS007','ACC007','Web','Transaction Error',
 'Transfer not reflected',
 'High','UNDER_REVIEW','2025-02-18 08:45:00','EMP001'),

('CMP025','CUS007','ACC007','Email','Online Banking',
 'Unable to download statements',
 'Medium','OPEN','2025-02-19 12:00:00','EMP002'),

('CMP026','CUS007','ACC007','Phone','Fee Dispute',
 'Investment fee concern',
 'Low','OPEN','2025-02-20 16:15:00','EMP007'),

-- CUS008 (1 additional complaint)
('CMP027','CUS008','ACC008','Web','Customer Service',
 'Agent disconnected call',
 'Low','OPEN','2025-02-21 10:00:00','EMP006'),

-- CUS009 (2 additional complaints, one NULL account)
('CMP028','CUS009','ACC009','Branch','Fraud Claim',
 'Suspicious transaction detected',
 'Critical','UNDER_REVIEW','2025-02-22 09:20:00','EMP007'),

('CMP029','CUS009',NULL,'Email','Fraud Claim',
 'Potential identity theft concern',
 'Critical','OPEN','2025-02-23 11:45:00','EMP007'),

-- CUS010 (1 additional complaint, NULL account)
('CMP030','CUS010',NULL,'Web','Service Delay',
 'No response to inquiry',
 'Medium','OPEN','2025-02-24 13:15:00','EMP006');


-- =====================================================
-- COMPLAINT STATUS HISTORY
-- =====================================================

INSERT INTO complaint_status_history
(complaint_id,old_status,new_status,changed_by,comments)
VALUES

('CMP011',NULL,'OPEN','EMP001','Complaint created'),
('CMP012','OPEN','UNDER_REVIEW','EMP002','Escalated for analyst review'),
('CMP013',NULL,'OPEN','EMP006','Complaint registered'),

('CMP014',NULL,'OPEN','EMP006','Complaint received'),
('CMP015','OPEN','IN_PROGRESS','EMP001','Investigation started'),

('CMP016','OPEN','UNDER_REVIEW','EMP001','Assigned for review'),
('CMP017',NULL,'OPEN','EMP002','Complaint registered'),
('CMP018',NULL,'OPEN','EMP006','Complaint logged'),

('CMP019',NULL,'OPEN','EMP007','Complaint opened'),

('CMP020',NULL,'OPEN','EMP002','Complaint created'),
('CMP021','OPEN','IN_PROGRESS','EMP001','Investigation started'),

('CMP022',NULL,'OPEN','EMP002','Complaint received'),
('CMP023',NULL,'OPEN','EMP006','General complaint logged'),

('CMP024','OPEN','UNDER_REVIEW','EMP001','Evidence collection started'),
('CMP025',NULL,'OPEN','EMP002','Complaint registered'),
('CMP026',NULL,'OPEN','EMP007','Complaint opened'),

('CMP027',NULL,'OPEN','EMP006','Complaint created'),

('CMP028','IN_PROGRESS','UNDER_REVIEW','EMP007',
 'Fraud investigation initiated'),

('CMP029',NULL,'OPEN','EMP007',
 'Potential fraud complaint registered'),

('CMP030',NULL,'OPEN','EMP006',
 'Complaint logged');
