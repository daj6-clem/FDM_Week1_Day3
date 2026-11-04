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
