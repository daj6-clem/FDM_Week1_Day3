import datetime as dt
from unittest.mock import Mock
from src.agent.tools import AgentTools
import pytest

@pytest.fixture
def tools():

    db = Mock()

    audit_log_repo = Mock()
    complaint_note_repo = Mock()
    recommendation_repo = Mock()
    review_decision_repo = Mock()
    review_request_repo = Mock()

    complaint_service = Mock()
    account_service = Mock()
    customer_service = Mock()

    retrieval_service = Mock()
    answer_service = Mock()

    return AgentTools(
        db=db,
        audit_log_repository=audit_log_repo,
        complaint_note_repository=complaint_note_repo,
        recommendation_repository=recommendation_repo,
        review_decision_repository=review_decision_repo,
        review_request_repository=review_request_repo,
        complaint_service=complaint_service,
        account_service=account_service,
        customer_service=customer_service,
        retrieval_service=retrieval_service,
        answer_service=answer_service
    )

def test_get_customer_returns_customer(tools):
    customer = Mock()

    tools.customer_service.get_by_id.return_value = customer

    result = tools.get_customer("CUST1")

    assert result == customer

    tools.customer_service.get_by_id.assert_called_once_with("CUST1")

def test_get_accounts_returns_accounts(tools):
    accounts = [Mock(), Mock()]

    tools.account_service.get_for_customer.return_value = accounts

    result = tools.get_accounts("CUST1")

    assert result == accounts

def test_get_complaint_returns_complaints(
    tools
):
    complaints = [Mock()]

    tools.complaint_service.get_for_customer.return_value = complaints

    result = tools.get_complaint("CUST1")

    assert result == complaints

def test_search_policy_returns_chunks(
    tools
):
    filters = Mock()

    filters.document_type = "Policy"
    filters.version = "1.0"
    filters.access_label = "Approved"

    chunks = ["chunk1", "chunk2"]

    tools.retrieval_service.retrieve.return_value = chunks

    result = tools.search_policy(
        "fees",
        filters,
        5
    )

    assert result == chunks

    tools.retrieval_service.retrieve.assert_called_once()

def test_create_case_note_success(
    tools
):
    complaint = Mock()

    complaint.assigned_analyst_id = "EMP001"

    tools.complaint_service.get_by_id.return_value = complaint

    result = tools.create_case_note(
        "CMP001",
        "test note",
        ["REF1"]
    )

    assert result["success"] is True

    tools.complaint_note_repository.create.assert_called_once()

    tools.audit_log_repository.create.assert_called_once()

def test_create_case_note_not_found(
    tools
):
    tools.complaint_service.get_by_id.return_value = None

    result = tools.create_case_note(
        "BAD_ID",
        "note",
        []
    )

    assert result["success"] is False
    assert (
        result["error"]["code"]
        == "COMPLAINT_NOT_FOUND"
    )

def test_request_approval_success(
    tools
):
    complaint = Mock()

    complaint.assigned_analyst_id = "EMP001"

    tools.complaint_service.get_by_id.return_value = complaint

    recommendation = Mock()

    recommendation.recommendation_id = "REC001"

    tools.recommendation_repository.create.return_value = (
        recommendation
    )

    result = tools.request_approval(
        complaint_id="CMP001",
        action="Refund fee",
        parameters=[],
        evidence_refs=[]
    )

    assert result["success"] is True

    tools.recommendation_repository.create.assert_called_once()

    tools.review_request_repository.create.assert_called_once()

def test_request_approval_complaint_not_found(
    tools
):
    tools.complaint_service.get_by_id.return_value = None

    recommendation = Mock()

    recommendation.recommendation_id = "REC001"

    tools.recommendation_repository.create.return_value = (
        recommendation
    )

    result = tools.request_approval(
        "BAD",
        "action",
        [],
        []
    )

    assert result["success"] is False

    assert (
        result["error"]["code"]
        == "COMPLAINT_NOT_FOUND"
    )

def test_record_approval_decision_success(
    tools
):
    review_request = Mock()

    tools.review_request_repository.get_by_id.return_value = (
        review_request
    )

    result = tools.record_approval_decision(
        "RR001",
        "APPROVED",
        "Valid recommendation"
    )

    assert result["success"] is True

    tools.review_decision_repository.create.assert_called_once()

    tools.review_request_repository.update.assert_called_once()

    assert review_request.status == "APPROVED"

def test_record_approval_decision_no_request(
    tools
):
    tools.review_request_repository.get_by_id.return_value = None

    result = tools.record_approval_decision(
        "MISSING",
        "APPROVED",
        "reason"
    )

    assert result["success"] is True

    tools.review_request_repository.update.assert_not_called()

def test_update_complaint_status(
    tools
):
    complaint = Mock()

    complaint.complaint_id = "CMP001"
    complaint.status = "UNDER_REVIEW"
    complaint.assigned_analyst_id = "EMP001"

    tools.complaint_service.change_status.return_value = (
        complaint
    )

    result = tools.update_complaint_status(
        "CMP001",
        "UNDER_REVIEW",
        "progressed"
    )

    assert result["status"] == "UNDER_REVIEW"

    tools.audit_log_repository.create.assert_called_once()

def test_close_complaint(
    tools
):
    complaint = Mock()

    complaint.complaint_id = "CMP001"

    tools.complaint_service.change_status.return_value = (
        complaint
    )

    result = tools.close_complaint(
        "CMP001",
        "Resolved",
        "2026-11-18",
        []
    )

    assert result["success"] is True

    assert result["data"]["status"] == "Closed"