### PURPOSE:
Provides semantic search over indexed policy documents using vector embeddings and ChromaDB. It accepts a natural-language query, optionally applies metadata filters, retrieves the most relevant document chunks, and optionally reranks the results. This contract defines expected inputs, outputs, validation rules, and error handling for the Retrieval Service.

### INPUT CONTRACT:
{
        "query" : "Should dates be reset to disguise age?",
        "top_k" : 5,
        "document_type" : "Policy",
        "version" : "2.0",
        "access_label" : "Internal",
        "rerank" : True
}

Validation:
- query must be non-empty string
- top_k must be positive int
- metadata filters optional
- all metadata filters applied together using AND logic
- rerank optional

### OUTPUT CONTRACT:
[
    {
        "text": "...",
        "score": 0.85,
        "rerank_score": 7,
        "metadata": {
            "document": "Customer Complaints Policy",
            "page": 3,
            "document_type": "policy",
            "version": "2026",
            "access_label": "internal"
        }
    }
]

- When rerank = True, results are sorted by rerank_score in descending order
- When rerank = False, results are sorted by vector retrieval order
- If no document chunks are found, service returns an empty list

### ERROR HANDLING:
- Empty/Invalid query: ValueError (Query must be non-empty string)
- Invalid top_k: ValueError (top_k must be positive integer)
- Unexpected embedding dimensions: RetrievalError (Generated query embedding does not match configured dimensions)
- Vector database unavailable: RetrievalError (Retrieval operation failed)