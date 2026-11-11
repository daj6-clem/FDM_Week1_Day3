import pytest
from unittest.mock import MagicMock

from src.rag.retrieval_service import RetrievalService, RetrievalError

@pytest.fixture
def retrieval_service():
    vector_store = MagicMock()
    embedding_service = MagicMock()

    embedding_service.dimensions = 1536
    embedding_service.embed_query.return_value = [0.1] * 1536

    service = RetrievalService(
        vector_store=vector_store,
        embedding_service=embedding_service
    )

    return service

def test_empty_query(retrieval_service):
    with pytest.raises(ValueError):
        retrieval_service.retrieve("")


def test_no_matches(retrieval_service):
    retrieval_service.collection.query.return_value={
        "documents":[[]],
        "distances":[[]],
        "metadatas": [[]]
    }

    results = retrieval_service.retrieve("How do I fly to Mars?")

    assert results == []

def test_vector_store_unavailable(retrieval_service):
    retrieval_service.collection.query.side_effect = Exception("Vector store unavailable.")

    with pytest.raises(RetrievalError, match="Vector store unavailable"):
        retrieval_service.retrieve("What is the leave policy?")