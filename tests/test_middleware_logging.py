from src.api.main import logging_middleware
from src.services.complaint_service import ComplaintService
from src.models.models import ComplaintStatus, Complaint
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from src.api.error_handlers.error_handlers import CustomerNotFoundException, InvalidStatusTransitionException
from src.services.customer_service import CustomerService

def test_get_customer_not_found():
    service = CustomerService()
    service.repository = Mock()

    service.repository.get_by_id.return_value = None

    with pytest.raises(CustomerNotFoundException):
        service.get_by_id(Mock(), "CUS999")

def test_invalid_transition():
    complaint = Complaint(
        complaint_id="CMP001",
        status = ComplaintStatus.CLOSED
    )

    with pytest.raises(InvalidStatusTransitionException):
        complaint.change_status(ComplaintStatus.OPEN)

def test_db_unavailable(monkeypatch):
    service = ComplaintService()

    def fake_db_failure(*args, **kwargs):
        raise ConnectionError("Database unavailable")

    service.customer_repo = Mock()
    service.customer_repo.get_by_id = fake_db_failure

    with pytest.raises(ConnectionError):
        service.create_complaint(Mock(), Mock())

def test_unexpected_error(monkeypatch):
    service = ComplaintService()

    service.customer_repo = Mock()
    service.customer_repo.get_by_id.side_effect = RuntimeError("Boom")

    with pytest.raises(RuntimeError):
        service.create_complaint(Mock(), Mock())