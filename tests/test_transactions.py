from fastapi.testclient import TestClient
from src.api.main import app
from src.models.models import Complaint, ComplaintStatusHistory
from data.connection import SessionLocal
from data.repositories.complaint_status_history_repository import ComplaintStatusHistoryRepository
import pytest
from datetime import datetime

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

#Run by going to terminal and typing pytest
def test_create_complaint_success(client, db_session):
    complaint = {
        "customer_id": "CUS001",
        "account_id": "ACC001",
        "channel": "Email",
        "category": "Service Delay",
        "complaint_text": "Test complaint",
        "priority": "Medium",
        "status": "Open",
        "received_at": datetime.now().isoformat(),
        "assigned_analyst_id": "EMP007"
    }
    response = client.post("/complaints", json=complaint)
    print(response.json())

    assert response.status_code == 201

    complaintCheck = db_session.query(Complaint).filter(Complaint.complaint_text == "Test complaint").first()
    history = (db_session.query(ComplaintStatusHistory)
               .filter(ComplaintStatusHistory.complaint_id 
                       == complaintCheck.complaint_id)
                .first())
    assert complaintCheck is not None
    assert history is not None
    assert history.complaint_id == complaintCheck.complaint_id

def test_create_complaint_rollback(client, db_session, monkeypatch):
    def fail_create(*args, **kwargs):
        raise Exception("Simulate failure")

    monkeypatch.setattr(
        ComplaintStatusHistoryRepository,
        "create",
        fail_create
    )

    complaint = {
        "customer_id": "CUS001",
        "account_id": "ACC001",
        "channel": "Email",
        "category": "Service Delay",
        "complaint_text": "Test rollback complaint",
        "priority": "Medium",
        "status": "Open",
        "received_at": datetime.now().isoformat(),
        "assigned_analyst_id": "EMP007"
    }

    response = client.post("/complaints", json = complaint)

    assert response.status_code == 500

    complaint_check = (
        db_session.query(Complaint)
        .filter(Complaint.complaint_text == "Test rollback complaint")
        .first()
    )

    assert complaint_check is None
