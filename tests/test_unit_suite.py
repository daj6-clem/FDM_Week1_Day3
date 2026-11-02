from src.services.complaint_service import ComplaintService
from src.models.models import Complaint, ComplaintStatus, Customer, Account, AccountStatus, Channel, Category
from unittest.mock import Mock
from fastapi import HTTPException
from datetime import datetime
from src.api.error_handlers.error_handlers import InvalidStatusTransitionException, CustomerNotFoundException, ComplaintNotFoundException
from src.api.schemas import ComplaintCreate
from pydantic import ValidationError


import pytest

### TEST VALID/INVALID STATUS TRANSITIONS
@pytest.mark.parametrize(
        "old_status,new_status",
        [
            (ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS),
            (ComplaintStatus.IN_PROGRESS, ComplaintStatus.UNDER_REVIEW),
            (ComplaintStatus.IN_PROGRESS, ComplaintStatus.CLOSED),
            (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.CLOSED),

        ]
)
def test_change_status_valid(old_status, new_status):
    complaint = Complaint(
        complaint_id = "CMP001",
        status = old_status
    )

    complaint.change_status(new_status)

    assert complaint.status == new_status

@pytest.mark.parametrize(
    "old_status,new_status",
    [
        (ComplaintStatus.OPEN, ComplaintStatus.OPEN),
        (ComplaintStatus.OPEN, ComplaintStatus.UNDER_REVIEW),
        (ComplaintStatus.OPEN, ComplaintStatus.CLOSED),

        (ComplaintStatus.IN_PROGRESS, ComplaintStatus.IN_PROGRESS),
        (ComplaintStatus.IN_PROGRESS, ComplaintStatus.OPEN),

        (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.UNDER_REVIEW),
        (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.IN_PROGRESS),
        (ComplaintStatus.UNDER_REVIEW, ComplaintStatus.OPEN),

        (ComplaintStatus.CLOSED, ComplaintStatus.CLOSED),
        (ComplaintStatus.CLOSED, ComplaintStatus.OPEN),
        (ComplaintStatus.CLOSED, ComplaintStatus.IN_PROGRESS),
        (ComplaintStatus.CLOSED, ComplaintStatus.UNDER_REVIEW),
    ]
)
def test_change_status_invalid(old_status, new_status):
    complaint = Complaint(
        complaint_id="CMP001",
        status=old_status
    )

    with pytest.raises(InvalidStatusTransitionException):
        complaint.change_status(new_status)

### TEST MISSING REQUIRED FIELDS
@pytest.mark.parametrize(
    "missing_field",
    [
        "customer_id",
        "channel",
        "category",
        "complaint_text",
        "status",
        "received_at",
    ]
)
def test_complaint_create_missing_required_fields(missing_field):
    complaint_data = {
        "customer_id": "CUS001",
        "account_id": "ACC001",
        "channel": Channel.Email,
        "category": Category.SERVICE_DELAY,
        "complaint_text": "Test Complaint",
        "priority": None,
        "status": ComplaintStatus.OPEN,
        "received_at": datetime(2025, 1, 1),
        "assigned_analyst_id": None
    }

    del complaint_data[missing_field]

    with pytest.raises(ValidationError):
        ComplaintCreate(**complaint_data)


### TEST MISSING CUSTOMER
class FakeCustomerRepository:
    def get_by_id(self, db, customer_id):

        if customer_id == "CUS001":
            return Customer(customer_id="CUS001",
                            first_name = "Test",
                            last_name = "Thompson",
                            email = "testthom@test.test",
                            segment = "Retail",
                            date_created = datetime.now())

        return None

class FakeComplaintRepository:
    def generate_complaint_id(self, db):
        return "CMP001"
    def create(self, db, complaint, complaint_id):
        complaint.complaint_id = complaint_id
        return complaint

class FakeCSHRepo:
    def create(self, db, complaint, old_status):
        return None

def test_create_complaint_success():
    service = ComplaintService()
    service.customer_repo = FakeCustomerRepository()
    service.complaint_repo = FakeComplaintRepository()
    service.csh_repo = FakeCSHRepo()

    complaint = Mock()
    complaint.customer_id = "CUS001"

    db = Mock()

    result = service.create_complaint(db, complaint)

    assert result.customer_id == "CUS001"
    assert result.complaint_id == "CMP001"


@pytest.mark.parametrize(
        "customer_id",
        [
            "CUS999",
            "CUS888",
            "CUS777"
        ]
)
def test_create_complaint_cus_dne(customer_id):
    service = ComplaintService()
    service.customer_repo = FakeCustomerRepository()

    complaint = Mock()
    complaint.customer_id = customer_id

    db = Mock()

    with pytest.raises(CustomerNotFoundException):
        service.create_complaint(db, complaint)

def test_get_for_cus_dne():
    service = ComplaintService()

    service.customer_repo = FakeCustomerRepository()
    db = Mock()

    with pytest.raises(CustomerNotFoundException):
        service.get_for_customer(db, "CUS999")

### TEST ESCALATION BOUNDARIES
def test_create_complaint_creates_csh():

    service = ComplaintService()

    service.customer_repo = FakeCustomerRepository()
    service.complaint_repo = FakeComplaintRepository()
    service.csh_repo = FakeCSHRepo()

    complaint = Mock()
    complaint.customer_id = "CUS001"

    db = Mock()

    service.create_complaint(db, complaint)

    db.commit.assert_called_once()
    db.rollback.assert_not_called()

def test_create_complaint_rolls_back():

    service = ComplaintService()

    service.customer_repo = FakeCustomerRepository()
    service.complaint_repo = FakeComplaintRepository()

    service.csh_repo = Mock()
    service.csh_repo.create.side_effect = Exception("boom")

    complaint = Mock()
    complaint.customer_id = "CUS001"

    db = Mock()

    with pytest.raises(Exception):
        service.create_complaint(db, complaint)

    db.rollback.assert_called_once()

def test_get_by_id_not_found():
    service = ComplaintService()
    service.complaint_repo = Mock()
    service.complaint_repo.get_by_id.return_value = None

    db = Mock()

    with pytest.raises(ComplaintNotFoundException):
        service.get_by_id(db, "CMP999")

### TEST SERVICE BEHAVIOR WITH FAKE REPOSITORIES
### TESTS MUST BE DETERMINISTIC
### TESTS MUST BE BEHAVIOR FOCUSED
### TESTS MUST USE PARAMETRIZATION
