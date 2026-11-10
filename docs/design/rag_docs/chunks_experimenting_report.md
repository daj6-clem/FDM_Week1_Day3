Smart Chunking will be chosen as the default strategy.

Pros:
- Higher total success rate (2/3)
- Works off of document structure
- Should be more flexible
- Preserves semantic units
- Preserves section content
- Better for structured documents like policy and procedure

Cons:
- Higher number of chunks
- takes longer
- Requires steady maintenance of chunking rules
- Can become too fragmented if too many rules are added
- Assumes documents are structured
- More complex code





===== CHUNK STATISTICS =====
Fixed chunk count: 187
Smart chunk count: 183

=================================
TESTING FIXED CHUNKING
=================================
==== Querying Chroma ====

========== CH-001 ==========
Query: When is supervisor approval required?
Expected: KB-002 | 3. Financial Redress Thresholds

ACTUAL RETRIEVED RESULTS:
1. KB-002 | 7. Boundary Examples
2. KB-002 | 2. Decision Principles
3. KB-002 | Detailed Worked Scenarios
4. KB-002 | 3. Financial Redress Thresholds
5. KB-010 | Detailed Worked Scenarios
6. KB-002 | 1. Purpose
7. KB-009 | 1. Purpose
8. KB-010 | Detailed Worked Scenarios
9. KB-007 | 5. Recommendation Format
10. KB-001 | 7. Investigation Procedure

Source match: True
Section match: True
==== Querying Chroma ====

========== CH-002 ==========
Query: What evidence is needed for a fee complaint?
Expected: KB-003 | 2. Required Intake Fields

ACTUAL RETRIEVED RESULTS:
1. KB-002 | 5. Approval Request Requirements
2. KB-010 | Detailed Worked Scenarios
3. KB-007 | 2. Investigation Planning
4. KB-001 | Detailed Worked Scenarios
5. KB-005 | 4. Resolution Communication
6. KB-007 | Detailed Worked Scenarios
7. KB-003 | Detailed Worked Scenarios
8. KB-001 | 3. Roles and Responsibilities
9. KB-003 | 6. Evidence and Communication
10. KB-005 | 2. Acknowledgement Content

Source match: True
Section match: False
==== Querying Chroma ====

========== CH-003 ==========
Query: When should suspected account takeover be escalated?
Expected: KB-004 | 4. Security Escalation Indicators

ACTUAL RETRIEVED RESULTS:
1. KB-003 | 1. Scope and Complaint Types
2. KB-002 | 1. Purpose
3. KB-004 | 5. Prohibited Behaviors
4. KB-009 | 1. Purpose
5. KB-009 | 1. Purpose
6. KB-003 | 7. Quality Checks
7. KB-002 | 4. Specialist Escalation Triggers
8. KB-001 | Detailed Worked Scenarios
9. KB-010 | Detailed Worked Scenarios
10. KB-007 | Detailed Worked Scenarios

Source match: True
Section match: False

Fixed Chunking Score: 1/3

=================================
TESTING SMART CHUNKING
=================================
==== Querying Chroma ====

========== CH-001 ==========
Query: When is supervisor approval required?
Expected: KB-002 | 3. Financial Redress Thresholds

ACTUAL RETRIEVED RESULTS:
1. KB-009 | 1. Purpose
2. KB-010 | Detailed Worked Scenarios
3. KB-010 | Detailed Worked Scenarios
4. KB-010 | Detailed Worked Scenarios
5. KB-010 | Detailed Worked Scenarios
6. KB-002 | 7. Boundary Examples
7. KB-002 | 1. Purpose
8. KB-002 | 3. Financial Redress Thresholds
9. KB-001 | 3. Roles and Responsibilities
10. KB-002 | 5. Approval Request Requirements

Source match: True
Section match: True
==== Querying Chroma ====

========== CH-002 ==========
Query: What evidence is needed for a fee complaint?
Expected: KB-003 | 2. Required Intake Fields

ACTUAL RETRIEVED RESULTS:
1. KB-003 | Detailed Worked Scenarios
2. KB-001 | Detailed Worked Scenarios
3. KB-003 | 6. Evidence and Communication
4. KB-010 | Detailed Worked Scenarios
5. KB-010 | Detailed Worked Scenarios
6. KB-002 | 5. Approval Request Requirements
7. KB-001 | 3. Roles and Responsibilities
8. KB-001 | Detailed Worked Scenarios
9. KB-001 | 2. Definitions
10. KB-005 | 2. Acknowledgement Content

Source match: True
Section match: False
==== Querying Chroma ====

========== CH-003 ==========
Query: When should suspected account takeover be escalated?
Expected: KB-004 | 4. Security Escalation Indicators

ACTUAL RETRIEVED RESULTS:
1. KB-010 | Detailed Worked Scenarios
2. KB-009 | 1. Purpose
3. KB-003 | 4. Common Root Causes
4. KB-010 | Detailed Worked Scenarios
5. KB-010 | Detailed Worked Scenarios
6. KB-002 | 1. Purpose
7. KB-004 | 4. Security Escalation Indicators
8. KB-004 | Detailed Worked Scenarios
9. KB-003 | 7. Quality Checks
10. KB-001 | Detailed Worked Scenarios

Source match: True
Section match: True

Smart Chunking Score: 2/3

=================================
FINAL COMPARISON
=================================
Fixed : 1/3
Smart : 2/3