NOTE: run with "python -m src.rag.ingestion_service"
        rebuild with "python -m src.rag.ingestion_service --rebuild"

Batch Size: 500
Duration: 8 seconds
    Ingestion main() start to finish
        Start: 2026-11-10 16:53:10,610 - Loaded 183 chunks
        Finish: 2026-11-10 16:53:18,767 - Validation report saved

LOGS:
==== Checking Manifest ====

========== VALIDATION SUMMARY ==========
Files accepted: 13
Files rejected: 0
File warnings:  0
========================================

===== EXTRACTED SECTIONS =====
KB-001 | Introduction
KB-001 | 1. Policy Objective and Scope
KB-001 | 2. Definitions
KB-001 | 3. Roles and Responsibilities
KB-001 | 4. Intake Standard
KB-001 | 5. Acknowledgement and Ownership
KB-001 | 6. Triage and Classification
KB-001 | 7. Investigation Procedure
KB-001 | 8. Resolution and Communication Standard
KB-001 | 9. Closure and Reopen Controls
KB-001 | 10. Quality Assurance and Audit
KB-001 | Detailed Worked Scenarios
KB-002 | Introduction
KB-002 | 1. Purpose
KB-002 | 2. Decision Principles
KB-002 | 3. Financial Redress Thresholds
KB-002 | 4. Specialist Escalation Triggers
KB-002 | 5. Approval Request Requirements
KB-002 | 6. Approval Decisions
KB-002 | 7. Boundary Examples
KB-002 | Detailed Worked Scenarios
KB-003 | Introduction
KB-003 | 1. Scope and Complaint Types
KB-003 | 2. Required Intake Fields
KB-003 | 3. Investigation Sequence
KB-003 | 4. Common Root Causes
KB-003 | 5. Redress and Approval
KB-003 | 6. Evidence and Communication
KB-003 | 7. Quality Checks
KB-003 | Detailed Worked Scenarios
KB-003 | Frequently Asked Operational Questions
KB-004 | Introduction
KB-004 | 1. Scope
KB-004 | 2. Intake and Diagnostic Evidence
KB-004 | 3. Standard Diagnostic Path
KB-004 | 4. Security Escalation Indicators
KB-004 | 5. Prohibited Behaviors
KB-004 | 6. Accessibility and Channel Needs
KB-004 | 7. Closure Evidence
KB-004 | Detailed Worked Scenarios
KB-004 | Frequently Asked Operational Questions
KB-005 | Introduction
KB-005 | 1. Service Principles
KB-005 | 2. Acknowledgement Content
KB-005 | 3. Status Updates
KB-005 | 4. Resolution Communication
KB-005 | 5. Accessibility
KB-005 | 6. Language Assistance
KB-005 | 7. Quality Review
KB-005 | Detailed Worked Scenarios
KB-005 | Frequently Asked Operational Questions
KB-006 | Introduction
KB-006 | 1. Scope
KB-006 | 2. Required Evidence
KB-006 | 3. Payment Posting Investigation
KB-006 | 4. Statement and Servicing Concerns
KB-006 | 5. Hardship and Sensitive Context
KB-006 | 6. Escalation and Redress
KB-006 | 7. Closure Checklist
KB-006 | Detailed Worked Scenarios
KB-006 | Frequently Asked Operational Questions
KB-007 | Introduction
KB-007 | 1. Purpose
KB-007 | 2. Investigation Planning
KB-007 | 3. Evidence Gathering
KB-007 | 4. Findings Format
KB-007 | 5. Recommendation Format
KB-007 | 6. Review Checklist
KB-007 | 7. Failure and Recovery
KB-007 | Detailed Worked Scenarios
KB-007 | Frequently Asked Operational Questions
KB-008 | Introduction
KB-008 | 1. Governance Principles
KB-008 | 2. Data Classification and Handling
KB-008 | 3. RAG Governance
KB-008 | 4. Tool and Agent Governance
KB-008 | 5. Logging and Tracing
KB-008 | 6. Evaluation Governance
KB-008 | 7. Security Testing
KB-008 | 8. Release Evidence
KB-008 | Detailed Worked Scenarios
KB-008 | Frequently Asked Operational Questions
KB-009 | Introduction
KB-009 | 1. Purpose
KB-010 | Introduction
KB-010 | 1. Use and Limitations
KB-010 | Detailed Worked Scenarios
KB-010 | Case Similarity Warning
BUL-2026-01 | Introduction
BUL-2026-01 | Bulletin Summary
BUL-2026-01 | Clarifications
BUL-2026-01 | Implementation Note
BUL-2026-02 | Introduction
BUL-2026-02 | Bulletin Summary
BUL-2026-02 | Required Controls
BUL-2026-02 | Release Test Requirements
KB-001-OLD | Introduction
KB-001-OLD | Status Notice
KB-001-OLD | Historical Content
KB-001-OLD | Historical Closure Rule

===== CHUNK STATISTICS =====
Smart chunk count: 183
2026-11-10 16:53:10,610 - Loaded 183 chunks
2026-11-10 16:53:11,277 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:11,304 - Batch 1:Sent 10, Received 10
2026-11-10 16:53:11,304 - Batch 1 processed(10 embeddings)
2026-11-10 16:53:11,619 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:11,648 - Batch 2:Sent 10, Received 10
2026-11-10 16:53:11,648 - Batch 2 processed(10 embeddings)
2026-11-10 16:53:12,080 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:12,102 - Batch 3:Sent 10, Received 10
2026-11-10 16:53:12,103 - Batch 3 processed(10 embeddings)
2026-11-10 16:53:12,442 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:12,461 - Batch 4:Sent 10, Received 10
2026-11-10 16:53:12,461 - Batch 4 processed(10 embeddings)
2026-11-10 16:53:12,739 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:12,769 - Batch 5:Sent 10, Received 10
2026-11-10 16:53:12,770 - Batch 5 processed(10 embeddings)
2026-11-10 16:53:13,121 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:13,129 - Batch 6:Sent 10, Received 10
2026-11-10 16:53:13,130 - Batch 6 processed(10 embeddings)
2026-11-10 16:53:13,556 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:13,582 - Batch 7:Sent 10, Received 10
2026-11-10 16:53:13,583 - Batch 7 processed(10 embeddings)
2026-11-10 16:53:14,012 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:14,042 - Batch 8:Sent 10, Received 10
2026-11-10 16:53:14,042 - Batch 8 processed(10 embeddings)
2026-11-10 16:53:14,436 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:14,443 - Batch 9:Sent 10, Received 10
2026-11-10 16:53:14,444 - Batch 9 processed(10 embeddings)
2026-11-10 16:53:14,728 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:14,738 - Batch 10:Sent 10, Received 10
2026-11-10 16:53:14,738 - Batch 10 processed(10 embeddings)
2026-11-10 16:53:15,132 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:15,156 - Batch 11:Sent 10, Received 10
2026-11-10 16:53:15,157 - Batch 11 processed(10 embeddings)
2026-11-10 16:53:15,442 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:15,447 - Batch 12:Sent 10, Received 10
2026-11-10 16:53:15,447 - Batch 12 processed(10 embeddings)
2026-11-10 16:53:16,016 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:16,028 - Batch 13:Sent 10, Received 10
2026-11-10 16:53:16,028 - Batch 13 processed(10 embeddings)
2026-11-10 16:53:16,364 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:16,395 - Batch 14:Sent 10, Received 10
2026-11-10 16:53:16,396 - Batch 14 processed(10 embeddings)
2026-11-10 16:53:16,723 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:16,736 - Batch 15:Sent 10, Received 10
2026-11-10 16:53:16,736 - Batch 15 processed(10 embeddings)
2026-11-10 16:53:17,061 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:17,093 - Batch 16:Sent 10, Received 10
2026-11-10 16:53:17,093 - Batch 16 processed(10 embeddings)
2026-11-10 16:53:17,489 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:17,498 - Batch 17:Sent 10, Received 10
2026-11-10 16:53:17,498 - Batch 17 processed(10 embeddings)
2026-11-10 16:53:17,809 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:17,829 - Batch 18:Sent 10, Received 10
2026-11-10 16:53:17,830 - Batch 18 processed(10 embeddings)
2026-11-10 16:53:18,145 - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2026-11-10 16:53:18,147 - Batch 19:Sent 3, Received 3
2026-11-10 16:53:18,148 - Batch 19 processed(3 embeddings)
2026-11-10 16:53:18,148 - Embedded 183 chunks

Embedded 183 chunks

===== EMBEDDING VALIDATION =====
Expected chunks: 183
Embedded chunks: 183
Missing chunks: 0
2026-11-10 16:53:18,307 - Persisting 183 embedded chunks
2026-11-10 16:53:18,678 - Vector batch processed: 183/183
2026-11-10 16:53:18,678 - Successfully persisted 183 vectors

Total vectors in database:183

================= INGESTION COMPLETE ==================
2026-11-10 16:53:18,722 - Starting vector index validation.
2026-11-10 16:53:18,723 - Chunk count: 183
2026-11-10 16:53:18,724 - Vector count: 183
2026-11-10 16:53:18,766 - ===== VECTOR INDEX VALIDATION =====
2026-11-10 16:53:18,766 - vector_count_matches_chunks: PASS
2026-11-10 16:53:18,766 - all_vectors_have_source_id: PASS
2026-11-10 16:53:18,767 - rebuild_has_no_duplicates: PASS
2026-11-10 16:53:18,767 - Overall status: PASS
2026-11-10 16:53:18,767 - Validation report saved: C:\Users\yaboi\Desktop\FDM\FDM_Week1_Day3\data\processed\vector_index_validation.json

===== VECTOR INDEX VALIDATION PASSED =====