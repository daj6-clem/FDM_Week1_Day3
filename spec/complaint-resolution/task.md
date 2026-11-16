**Backend Tasks**

- Parse customer_id from complaint

- Parse account_id from complaint

- Parse complaint_id from complaint

- Parse transactoin_id from complaint

- Parse fee_id from complaint

- Parse request_id from complaint

- Update Status History upon receiving complaint

- Use RAG to obtain transaction-dispute procedure

- Use RAG to obtain escalation matrix

- Use RAG to obtain document title

- Use RAG to obtain version

- Use Rag to obtain effective date

- Use Rag to obtain section

- Compare complaint information to RAG information

- Combine compared information into evidence package

- Route evidence package to human for review

- Record reviewer information

- Send customer response

- Create complaint and complaint status history in single transaction, rollback on failure

**Frontend Tasks**

- The frontend requests the summarized version of the claim

- Grab the AI suggestion from the backend.

- Correctly display the summary/suggestion.

- Button for escalation that pings a supervisor.

- Button for accepting claim.

- Button for denying claim.

**Testing Tasks**

- Unit tests for validation

- Integration tests

- Test proper complaint emails

- Test complaint emails that are missing information

**Documentation & Validation Tasks**

- Every claim has an audit trail from first entered to final decision.


### RAG IMPLEMENTATION TASKS:
TASKS: EACH TASK REFERENCES A SECTION IN THE SPECIFICATION
1. Load policy PDFs
    - See Spec Preconditions
2. Create chunking service
    - See Spec Preconditions: "Load policy into a vector database"
3. Generate embeddings
    - See Spec Preconditions: "Load policy into a vector database"
4. Implement vector search
    - See Flow 2: "Retrieve relevant documents"
    - See Rules: Return top 3 matches
5. Implement Answer
    - See Flow 4: Generate Answer
    - Rules: Base recommendations on policy
5. Implement citation formatting
    - See Flow 5: "Return answer with citations"
    - Rules: Source Document
    - Rules: Section
    - Rules: Effective Date
    - Rules: Policy Version
6. Implement abstention logic:
    - See Rules 5: "If evidence is insufficient, the system must abstain from providing an answer."
    - Rules: Catch questions not about policy, do not answer
    - Rules: Do not supply legal advice
    - Errors: Document unavailable, do not answer


### AGENT IMPLEMENTATION TASKS:
1. Read in complaint narrative and identifiers
- Flow 1
- Agent will not mix up information from different complaints
2. Classify issue
- Flow 2
- Issue should be classified as fee complaint or not at all
- Agent will not classify issues with low confidence
3. Identify required evidence
- Flow 3
- Account Status
- Transaction Timing
- Deposit Timing
- Fee History
- Fee-Review Policy
4. Call approved SQL tools
- Flow 4
- Extract operational facts
- Do not extract irrelevant facts
- Agent can only call approved SQL tools
- Agent cannot write to SQL or RAG databases except to record changes once a decision has been made
5. Call approved RAG tools
- Flow 5
- Retrieve only relevant policy passages
- Agent can only call approved RAG tools
- Agent cannot write to SQL or RAG databases except to record changes once a decision has been made
6. Check whether required evidence is missing or contradictory
- Flow 6
7. Preapare case summary
- Flow 7
- Prepare verified facts
- Prepare retrieved policy evidence
- Prepare generated analysis
- Agent's case summar will separate verified facts, retrieved policy evidence, and generated analysis
8. Propose next action
- Flow 8
- Agent cannot take independent action
9. Pause and create supervisor-review request
- Flow 9
- Fee reversal is a controlled action
- Agent must wait after creating supervisor-review request
10. Continue once supervisor-review request has been finalized
- Flow 10
- Request approved
- Request rejected
- Changes requested
- Agent will not continue until supervisor approves, rejects, or requests changes
11. Record relevant details
- Flow 11
- Record Decision
- Record status update
- Record audit history
- Agent must record all decisions, status updates, and audit histories