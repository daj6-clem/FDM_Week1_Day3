**Overview:**

- The Banking Complaint Resolution Assistant is for the Complaint Analyst to understand the complaint, verfiy the customer's history, locate the applicable policy and prepare a recommendation.

- Complaint analysts, customers, and supervisors will be the only ones interacting with the tool.

- This makes information handling faster and supports the professional judgements of complaint analysts in handling complaints.

**Scope**
- Get complaint
- Parse complaint
- Classify issues with medium confidence
- Identify required evidence
- Retrieve facts and policy
- Check for missing evidence
- Prepare case summary
- Propose next action
- View customer
- View Account
- View complaint
- Get customer account history
- Search Policy
- Cite Policy
- Create Review Request
- Update case status
- Triage case
- Identify missing information
- Draft Customer Response
- Record Audit event
- Propose next action
- Pause for human review
- Record decision, status update, and audit history

**Non-goals**
- Using real customer or production banking data.
- Automatically making final legal, regulatory, fraud, credit or compensation decisions.
- Giving the model unrestricted database or system access.
- Treating generated text as policy evidence without a valid source citation.
- Building every possible banking complaint process or product integration.

**Actors**
- Complaint Analyst

  - Review intake

  - Investigate evidence

  - Prepare recommendation

  - Communicate outcome

  - Escalate

  - Condition: Can view emails and System summaries, can send cases to Supervisors

- Supervisor/Reviewer

  - Review escalated/sensitive cases and approve/reject proposed action

  - Condition: Only views escalated/sensitive cases

- Agent

  - Parses complaint emails, gathers customer information, search/cite policy, triage, proposes actions for review

  - Condition: can only parse and view emails, cannot take actions

**Preconditions**
- The customer has an account with the bank.
- Established complaint narratives loaded into system
- Classification requirements loaded into system
- The customer issued a complaint via email, phone, branch, and web channels.

**Core Flows**
- Complaint Status Lifecycle and Valid Transitions:
1. OPEN -> IN PROGRESS
2. IN PROGRESS -> UNDER REVIEW
3. IN PROGRESS -> CLOSED
4. UNDER REVIEW -> CLOSED
5. CLOSED -> no further transitions

- The expected behavior:
1. The complaint has been received.

2. Does the complaint have the required data?

   1. If No, then request missing information/manual triage.

   2. If Yes Move to Step 3.

3. Does the complaint report an immediate safety, active account takeover, repeated unauthorized activity or inability to secure?

   3. If yes move to Step 7

   4. If No move to Step 4

4. Is the amount >= CAD $2,500 OR amount >= CAD $1,000 plus an unauthorized indicator?

   5. If yes move to Step 8

   6. If no move to Step 5

5. Is the amount CAD $500-$2,4999.99?

   7. If yes move to Step 9

   8. If no move to Step 6

6. Complaint enters Standard Queue. Move to Step 10.

7. Complaint enters Critical Queue (Immediate fraud/security and human review) Move to Step 10.

8. Complaint enters High Queue (Expedited analyst queue) Move to Step 10.

9. Complaint enters Medium Queue (Prompt analyst queue) Move to Step 10.

10. Sort the Complaints from Critical/High/Medium/Standard.

11. Retrieve structured facts + approved procedure.

12. Prepare evidence package.

13. Human reviewer decision; Complaint Analyst handles things below Critical, Supervisor handles Critical.

14. Approved response, audit trail, and closure.

**Business** **Rules**
- Assistant summaries require a preexisting email
- A summary requires a complaint id, a customer id, a customer statement, a transaction, additional indicators, requested outcome, and related policy
- Complaint Creation and initial status-history creation must succeed or fail together
- Partial creation prohibited

**Error Conditions** **and Edge Cases**
- Edge cases
- Invalid inputs
- Conflicting states
- Forbidden actions
- Exact error codes or categories
- Invalid ‘complaintId’ format -> 400, field=”complaintId"
- Invalid ‘accountId’ format -> 400, field=”accountId”
- Missing or invalid ‘transaction’-> 400, field =”transactionId”
- Missing or invalid ‘fee’->400, field=”feeId”
- Missing or invalid ‘request’->400, field=”requestId”
- All API errors return code, message, correlation_id

**NFRs**

- Audit logs exist for each customer's complaint.
- The latency is less than 1min for each complaint
- No sensitive information being disclosed to people uninvolved.
- Log: timestamp, level, correlation_id, operation, outcome, duration_ms
- Do not log: passwords, api keys, complete customer records, raw complaint narratives


**High-Level Interface expectation**

- Intake: receive and record the complaint narrative and available identifiers

- Triage: classify the complaint, assess urgency, and identify missing information

- Investigation: retrieve structured history and relevant approved policy evidence.

- Recommendation: prepare a grounded summary and proposed next action.

- Review and approval: route sensitive or escalated cases to a responsible human reviewer.

- Response and closure: communicate the approved outcome and retain evidence, status and audit history. 

**Domain Rules:**

- All ids must be unique

- Severity is determined from the company policy

- Escalation is determined from company policy

- All possible information should appear in the summary to help Complaint Analysts make the best possible judgements

**Success Criteria:**

- Given 100 working complaints, the tool will be able to correctly parse the necessary information, perform triage, draft the customer response, and wait for human review 95 out of 100 times.

- Give a complaint with missing information, the tool will be able to determine what information is missing, throw an exception, and then leave the complaint for human review.

**Security Constraints:**
- Protected from SQL Injection attacks
- Assistant must forget customer data after each case summary
- Staff has to be authorized to view customer data

**Audit Constraints:**

- Records all staff involved in approvals and denials

- Records all staff handling a claim

- Records all time logs for claim arrivals and response departure

- Records severity and transfers to higher priority

- Records location information

**Reliability Constraints:**

- Model should be at least 95% accurate in parsing patient information

- Model should be at least 95% accurate in parsing claims policy

- Models should be at least 95% accurate in judging severity


### RAG SPEC OVERVIEW:
Policy Knowledge Service provides grounded answers to complaint-related questions using approved policy documents. It provides an answer and a recommendation on how to move forward.

### SCOPE:
- Answer complaint policy questions
- Return citations
- Search approved policy documents
- Provide next steps forward

### NON-GOALS:
- Provide legal advice
- Create new company policy
- Answer questions outside approved documents
- Make decisions on policy

### ACTORS:
- Complaint Analyst
- Team Lead
- Complaint Suppport Agent
- Supervisor

### PRECONDITIONS:
- Established list of policies loaded into the system
- List of policies stored in vector database
- Policies chunked
- Policy embeddings
- Question asked related to policy
- User is authenticated and authorized
- Policy index is up to date
- LLM service is available

### FLOWS:
1. User asks a question
2. Retrieve relevant documents
3. Context sent to LLM
4. Answer generated
5. Return answer with citations

### RULES:
- Only approved policy documents will be searched
- System must retrieve top 3 most relevant documents
- Retrieved chunks must be included as citations
- Every answer must contain at least one citation
- If evidence is insufficient, the system must abstain from providing an answer
- Recommendations must be based only on policy
- Legal advice must not be supplied
- System must not answer questions unrelated to policy
- System must clearly distinguish between Answers, Citations, and Recommendations
- Citations must reference source document name
- Citations must reference chunk/sections
- Citations must correspond to the answer presented
- Every answer must cite the source document and section
- Every answer must cite the policy version
- Every answer must cite the effective date
- Every answer must provide certainty/uncertainty

### ERRORS:
- No matching policy found
- Document unavailable
- Too little evidence

### NFRs:
- Answer returned within 5 seconds.
- 95% of requests complete within 5 seconds
- Must support 50 concurrent users
- Retrieval failures handled gracefully
- No document failures may crash the service
- All requests must be logged
- Policy documents are stored securely
- New policy documents can be added without code changes
- Policy index can be refreshed without downtime

### API EXPECTATIONS:
- REST API
- Invalid Request -> 404
- Policy repository unavailable -> 503

### ACCEPTANCE CRITERIA:
- Citation Requirement: every answer must contain at least one citation.
- Retrieval Requirement: Top 3 relevant document chunks must be returned.
- Abstentation Requirement: If the AI Agent cannot find sufficient evidence, it must say that it could not find enough information int he approved policy sources.
- Questions unrelated to policy are rejected or abstained from
- Every question and answer should be viewable in logs
- Every answer must cite the source document and section
- Every answer must cite the policy version
- Every answer must cite the effective date
- API and backend will pass unit and integration tests for business rules and NFRs



### AGENT SPEC OVERVIEW:
The Agent should coordinate bounded investigation steps, using approved capabilities to read in complaint narratives, classify them, and retrieve required information. It will then create a summary, propose a next action, and pause for supervisor review. Once reviewed, it will record the decision, status update, and audit history.

### SCOPE:
- Read in complaints and identifiers
- Classify issues with medium confidence
- Identify required evidence
- Retreive facts and policy
- Check for missing evidence
- Prepare case summary
- Propose next action
- Create supervisor-review request
- Wait for review
- Record decision, status update, and audit history

### NON-GOALS:
- Agent does not replace SQL, RAG, or the human reviewer
- Agent will concede priority to fixed workflow whenever the workflow sequence is predictable
- Agent will not act independently
- Agent will not provide legal advice
- Agent will not create new evidence, policy, or SQL entries

### ACTORS:
- Agent
- Complaint Analyst
- Supervisor

### PRECONDITIONS:
- Established complaint narratives loaded into system
- Classification requirements loaded into system

### FLOWS:
1.	Read the complaint narrative and identifiers.
2.	Classify the issue as a fee complaint with medium confidence.
3.	Identify required evidence: account status, transaction timing, deposit timing, fee history and fee-review policy.
4.	Call approved SQL tools to retrieve exact operational facts.
5.	Call the RAG tool to retrieve relevant policy passages.
6.	Check whether required evidence is missing or contradictory.
7.	Prepare a case summary that separates verified facts, retrieved policy evidence and generated analysis.
8.	Propose a next action.
9.	Pause and create a supervisor-review request because a fee reversal is a controlled action.
10.	Continue only after the supervisor approves, rejects or requests changes.
11.	Record the decision, status update and audit history.

### RULES:
- Agent cannot write to SQL or RAG databases except to record changes once a decision has been made
- Agent will not mix up information from different complaints
- Agent will not classify issues with low confidence
- Agent's case summary will separate verified facts, retrieved poilcy evidence, and generated analysis
- Agent will only call approved tools
- Agent cannot take independent action on cases
- Agent must wait after creating the supervisor review request
- Agent will not continue until supervisor approves, rejects, or requests changes
- Agent must record all decisions, status updates, and audit histories

### ERRORS:
- Insufficient information is returned
- Failure to access SQL or RAG
- Failure to read in complaint narrative
- MCP tool timeout
- Model rate limit
- Invalid state transition
- Approval rejected

### NFRs:
- Agent will be able to retrieve all present complaing narrative identifiers with 95% accuracy
- Agent will flag cases with missing evidence 99% of the time
- Agent will return a response within two minutes
- All decisions, status updates, and audit histories must be recorded
- Databases are accessed in a secure manner

### ACCEPTANCE CRITERIA:
- Given a complaint narrative and complaint identifier are available in the system, when the agent begins processing a complaint, then it reads the narrative and associated identifiers and associates all retrieved information with that complaint
- Given a complaint narrative has been read, when the agent performs classification, then it classifies the complaint as a fee complaint only when confidence meets the configured threshold or higher
- Given a fee complaint has been classified, when the agent determines evidence requirements, then it identifies account status, transaction timing, deposit timing, fee history, and applicable policy as required evidence
- Given required evidence has been identified, when the agent retrieves operational information, then it uses only approved SQL tools and retrieves available facts relevant to the complaint
- Given operational facts have been retrieved, when the agent seeks policy guidance, then it uses the approved rag tool to retrieve relevant policy passages associated with the complaint
- Given facts and policy evidence have been retrieved, when the agent validates case completeness, then it identifies and flags any missing, incomplete, or contradictory evidence
- Given sufficient information has been gathered, when the agent creates a case summary, the summary clearly separates verified facts, retrieved policy evidence, and agent-generated analysis
- Given a case summary has been created, when the agente evaluates the complaint, then it proposes a next action based only on retrieved facts and policy evidence
- Given a proposed action has been generated, when the action requires review, then the agent creates a supervisor review request containing the case summary, evidence, and recommended action
- Given a supervisor review request exists, when the request is submitted, then the agent puases processing and performs no actions until a supervisor decision is made
- Given a supervisor decision is received, when the decision is approve, reject, or request changes, then the agent records the decision and updates the case status accordingly
- Given any material action occurs during case processing, when the action completes, then the agent records an auditable history entry containing the action performed, timestamp, and status
- Given the agent required external information, when it retrieves data, then it only uses approved SQL and RAG tools
- Given the agent recommends a fee reversal or other controlled action, when supervisor approval has not been received, then the agent does not execute or authorize the action
- Given complaint processing is underway, when the agent accesses sql or rag resources, then it performs read-only operations and does not modify source data
- Given a complaint narrative cannot be read, when processing begins, then the agent records an error, stops processing, and reports the failure
- Given required tools are unavailable, when retrieval is attempted, then the agent records the failure, notifies the user, and does not generate a final recommendation using incomplete data
- Given required evidence cannot be obtained, when case review is performed, then the agent flags the complaint as requiring additional evidence before recommendation
- The agent correctly retrieves complaint identifiers in at leats 95% of cases
- The agent correct flags missing evidence in at leats 99% of test cases containing incomplete evidence
- The agent completes complaint processing and review-request creation within 2 minutes for 95% of test cases
- 100% of supervisor decisions, status changes, and review actions are recorded in audit history
- All SQL and RAG access occurs through approved authenticated interfaces and complies with organizational security controls