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
    - Flow six

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