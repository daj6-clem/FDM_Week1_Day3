### OVERVIEW:
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