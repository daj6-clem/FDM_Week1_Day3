
from fastapi import APIRouter, HTTPException, Depends

from src.dependencies import (
    get_ingestion_service,
    get_retrieval_service,
    get_answer_service
)

from src.api.schemas import PolicyQuery
from src.rag.retrieval_service import RetrievalService
from src.rag.answer_service import AnswerService

router = APIRouter()


@router.post("/policy/query")
def query_policy(
    request: PolicyQuery,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    answer_service: AnswerService = Depends(get_answer_service)
):

    chunks = retrieval_service.retrieve(
        query=request.question,
        top_k=5,
        document_type = request.document_type,
        version = request.version,
        access_label = request.access_label,
        rerank=True
    )

    print("\n==== RETREIVAL RESULTS ====")

    for chunk in chunks:
        print(chunk["chunk_id"],
              chunk["score"])

    response = answer_service.generate_answer(
        question=request.question,
        chunks=chunks
    )

    return response

@router.post("/policy/ingest_to_store")
def ingest_policy(
    ingestion_service: IngestionService = Depends(
        get_ingestion_service
    )
):

    result = ingestion_service.ingest_to_vector_store(
        directory_path="docs/design/rag_docs/"
    )

    return {
        "status": "success"
    }