
import json
import pytest

from pathlib import Path
from unittest.mock import MagicMock

from src.rag.answer_service import AnswerService
from src.rag.retrieval_service import RetrievalService
from src.rag.citations import CitationFormatter


@pytest.fixture
def test_cases():
    path = (
        Path(__file__).parent
        / "grounded_answer_cases.json"
    )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def retrieval_service():

    service = MagicMock(spec=RetrievalService)

    evidence = [
        {
            "chunk_id": "chunk_001",
            "text": (
                "Proposed compensation outside "
                "approved guidelines requires "
                "supervisor approval."
            ),
            "score": 0.89,
            "metadata": {
                "document_id": "KB-002",
                "title": "Compensation Policy",
                "source_file": "compensation_policy.pdf",
                "section": "Supervisor Approval",
                "version": "2.0",
                "effective_date": "2026-01-01"
            }
        }
    ]

    def retrieve(**kwargs):

        query = kwargs["query"].lower()

        if "compensation" in query:
            return evidence

        return []

    service.retrieve.side_effect = retrieve

    return service


@pytest.fixture
def answer_service():

    client = MagicMock()
    formatter = MagicMock(spec=CitationFormatter)

    return AnswerService(
        client=client,
        model="gpt-4o",
        citation_formatter=formatter,
        min_retrieval_score=0.65,
    )


@pytest.mark.parametrize(
    "case_index",
    [0, 1, 2],
    ids=["GA-001", "GA-002", "GA-003"]
)
def test_grounded_answers(
    case_index,
    test_cases,
    retrieval_service,
    answer_service
):

    case = test_cases[case_index]

    question = case["question"]

    # Step 1: Retrieve evidence
    chunks = retrieval_service.retrieve(
        query=question,
        top_k=5,
        document_type="Policy",
        version="2.0",
        access_label="Internal",
        rerank=True
    )

    # Step 2: Configure LLM response
    if chunks:

        expected_limitation = case.get(
            "expected_limitation"
        )

        llm_response = {
            "answer": (
                "Proposed compensation outside "
                "approved guidelines requires "
                "supervisor approval."
            ),
            "supported": True,
            "evidence": ["chunk_001"],
            "limitations": (
                [expected_limitation]
                if expected_limitation
                else []
            )
        }

        answer_service.client.chat.completions.create.return_value = (
            MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content=json.dumps(llm_response)
                        )
                    )
                ]
            )
        )

    # Step 3: Generate answer
    response = answer_service.generate_answer(
        question=question,
        chunks=chunks
    )

    # Step 4: Validate support status
    assert response["supported"] == case["supported"]

    # Step 5: Validate evidence references
    expected_source = case.get("expected_source_id")

    if expected_source is None:
        assert response.get("evidence", []) == []
        assert response.get("citations", []) == []

    else:
        evidence_ids = response.get("evidence", [])

        actual_sources = {
            chunk["metadata"]["document_id"]
            for chunk in chunks
            if chunk["chunk_id"] in evidence_ids
        }

        assert expected_source in actual_sources

    # Step 6: Validate limitations
    expected_limitation = case.get(
        "expected_limitation"
    )

    if expected_limitation:

        actual_limitations = " ".join(
            response["limitations"]
        )

        assert expected_limitation.lower() in (
            actual_limitations.lower()
        )

    # Step 7: Verify LLM invocation
    llm_call = (
        answer_service.client.chat.completions.create
    )

    if chunks:
        llm_call.assert_called_once()
    else:
        llm_call.assert_not_called()
