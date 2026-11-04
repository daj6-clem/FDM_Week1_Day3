### OVERVIEW:
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
- New policy documetns can be added without code changes
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

