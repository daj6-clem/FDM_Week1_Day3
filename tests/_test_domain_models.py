from fastapi.testclient import TestClient
from src.api.main import app
from src.models.models import Complaint, Account, AccountStatus, ComplaintStatus
from data.connection import SessionLocal
from data.repositories.complaint_status_history_repository import ComplaintStatusHistoryRepository
import pytest
from datetime import datetime

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# TEST VALID AND INVALID STATES FOR models.py

def test_account_active_inactive():
    account = Account(status = AccountStatus.ACTIVE)

    account.change_status(AccountStatus.INACTIVE)

    assert account.status == AccountStatus.INACTIVE

def test_account_inactive_active():
    account = Account(status = AccountStatus.INACTIVE)

    account.change_status(AccountStatus.ACTIVE)

    assert account.status == AccountStatus.ACTIVE

def test_account_active_active():
    account = Account(status = AccountStatus.ACTIVE)

    with pytest.raises(ValueError):
        account.change_status(AccountStatus.ACTIVE)

def test_complaint_open_inprogress():
    complaint = Complaint(status = ComplaintStatus.OPEN)

    complaint.change_status(ComplaintStatus.IN_PROGRESS)

    assert complaint.status == ComplaintStatus.IN_PROGRESS

def test_complaint_inprogress_underreview():
    complaint = Complaint(status = ComplaintStatus.IN_PROGRESS)

    complaint.change_status(ComplaintStatus.UNDER_REVIEW)

    assert complaint.status == ComplaintStatus.UNDER_REVIEW

def test_complaint_underreview_closed():
    complaint = Complaint(status = ComplaintStatus.UNDER_REVIEW)

    complaint.change_status(ComplaintStatus.CLOSED)

    assert complaint.status == ComplaintStatus.CLOSED

def test_complaint_inprogress_closed():
    complaint = Complaint(status = ComplaintStatus.IN_PROGRESS)

    complaint.change_status(ComplaintStatus.CLOSED)

    assert complaint.status == ComplaintStatus.CLOSED

def test_complaint_open_closed():
    complaint = Complaint(status = ComplaintStatus.OPEN)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.CLOSED)

def test_complaint_open_underreview():
    complaint = Complaint(status = ComplaintStatus.OPEN)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.UNDER_REVIEW)

def test_complaint_inprogress_open():
    complaint = Complaint(status = ComplaintStatus.IN_PROGRESS)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.OPEN)

def test_complaint_underreview_open():
    complaint = Complaint(status = ComplaintStatus.UNDER_REVIEW)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.OPEN)

def test_complaint_underreview_inprogress():
    complaint = Complaint(status = ComplaintStatus.UNDER_REVIEW)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.IN_PROGRESS)

def test_complaint_closed_open():
    complaint = Complaint(status = ComplaintStatus.CLOSED)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.OPEN)

def test_complaint_closed_inprogress():
    complaint = Complaint(status = ComplaintStatus.CLOSED)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.IN_PROGRESS)

def test_complaint_closed_underreview():
    complaint = Complaint(status = ComplaintStatus.CLOSED)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.UNDER_REVIEW)

def test_complaint_closed_closed():
    complaint = Complaint(status = ComplaintStatus.CLOSED)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.CLOSED)

def test_complaint_open_open():
    complaint = Complaint(status = ComplaintStatus.OPEN)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.OPEN)

def test_complaint_inprogress_inprogress():
    complaint = Complaint(status = ComplaintStatus.IN_PROGRESS)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.IN_PROGRESS)

def test_complaint_underreview_underreview():
    complaint = Complaint(status = ComplaintStatus.UNDER_REVIEW)

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.UNDER_REVIEW)