### TOOL CATALOGUE

get_customer
- Purpose: Retrieves a synthetic customer by customer_id
- Inputs: customer_id:string
- Outputs: customer record or not_found
- Allowed role: Analyst, Supervisor
- Controls: Read-only; BR-004/027

get_accounts
- Purpose: List accounts for a verified customer
- Inputs: customer_id:string
- Outputs: account summaries
- Allowed role: Analyst, Supervisor
- Controls: Read-only; minimize fields

get_complaint
- Purpose: Retrieve complaint and status history
- Inputs: customer_id:string
- Outputs: complaint details/history
- Allowed role: Analyst, Supervisor
- Controls: Read-only

search_policy
- Purpose: Retrieve approved policy chunks
- Inputs: query:string, filters:object, top_k:int
- Outputs: ranked evidence with metadata
- Allowed role: Analyst, Supervisor
- Controls: Current version/access filters

create_case_note
- Purpose: Add analyst note
- Inputs: complaint_id, note, evidence_refs
- Outputs: note ID/audit event
- Allowed role: Analyst, Supervisor
- Controls: Parameterized; no secrets

request_approval
- Purpose: Request approval for current proposed action
- Inputs: complaint_id, action, parameters, evidence_refs
- Outputs: approval request ID/status
- Allowed role: Analyst
- Controls: Case-specific; BR-029

record_approval_decision
- Purpose: Approve/reject request
- Inputs: approval_id, decision, reason
- Outputs: decision/audit event
- Allowed role: Supervisor
- Controls: Human only

update_complaint_status
- Purpose: Apply allowed status transition
- Inputs: complaint_id, target_status, reason
- Outputs: new status/audit event
- Allowed role: Authorized role
- Controls: Transition validation

close_complaint
- Purpose: Close case after evidence/approval validation
- Inputs: complaint_id, resolution, communication_date, evidence_refs
- Outputs: closed case/audit event
- Allowed role: Supervisor
- Controls: Sensitive; BR-018/038


