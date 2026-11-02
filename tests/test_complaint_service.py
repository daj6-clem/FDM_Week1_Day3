from src.services.complaint_service import ComplaintService
from src.models.models import Complaint, ComplaintStatus
from unittest.mock import Mock
from fastapi import HTTPException
import pytest

def test_create_valid():
    service = ComplaintService()

    service.customer_repo = Mock()
    service.complaint_repo = Mock()
    service.csh_repo = Mock()

    complaint_request = Mock()
    complaint_request.customer_id = "CUS999"

    createdComp = Mock()

    service.customer_repo.get_by_id.return_value = Mock()
    service.complaint_repo.generate_complaint_id.return_value = "CMP999"
    service.complaint_repo.create.return_value = createdComp

    db = Mock()

    result = service.create_complaint(db, complaint_request)

    assert createdComp == result
    db.commit.assert_called_once()


def test_create_complaint_cus_not_found():
    service = ComplaintService()

    service.customer_repo = Mock()

    complaint_request = Mock()
    complaint_request.customer_id = "CUS999"

    service.customer_repo.get_by_id.return_value = None

    with pytest.raises(ValueError):
        service.create_complaint(
            Mock(),
            complaint_request
        )

def test_change_status_valid():
    service = ComplaintService()

    complaint = Complaint(complaint_id = "CMP999",
                          status = ComplaintStatus.OPEN)

    service.complaint_repo = Mock()
    service.csh_repo = Mock()

    service.complaint_repo.get_by_id.return_value = complaint

    db = Mock()

    service.change_status(db, complaint.complaint_id, ComplaintStatus.IN_PROGRESS)

    assert complaint.status == ComplaintStatus.IN_PROGRESS



def test_change_status_invalid_transition():
    service = ComplaintService()

    complaint = Complaint(
        status = ComplaintStatus.OPEN
    )

    service.complaint_repo = Mock()
    service.csh_repo = Mock()

    service.complaint_repo.get_by_id.return_value = complaint

    db = Mock()

    with pytest.raises(HTTPException) as exc:
        service.change_status(
            db,
            "CMP001",
            ComplaintStatus.CLOSED
        )

    assert exc.value.status_code == 409

def test_change_status_cmp_dne():
    service = ComplaintService()

    service.complaint_repo = Mock()

    db = Mock()

    service.complaint_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.change_status(
            db,
            "CUS999",
            ComplaintStatus.OPEN
        )

    assert exc.value.status_code == 404