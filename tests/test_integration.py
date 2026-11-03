from src.models.models import Customer, Complaint, ComplaintStatus, Channel, Category
import pytest

def test_customer_get_success(client, seeded_customer):
    response = client.get("/customers/CUS001")

    body = response.json()

    assert response.status_code == 200
    assert body["customer_id"] == "CUS001"

def test_customer_get_dne(client):
    response = client.get("/customers/CUS999")

    assert response.status_code == 404




def test_create_complaint_success(client, db_session, seeded_customer):
    complaintData = {
        "customer_id":"CUS001",
        "account_id":"ACC001",
        "channel":"Email",
        "category":"Service Delay",
        "complaint_text":"Integration test",
        "priority":"Low",
        "status": "Open",
        "received_at": "2025-01-01T00:00:00",
        "assigned_analyst_id":"EMP007"
    }

    response = client.post("/complaints", json=complaintData)

    assert response.status_code == 201

    body = response.json()

    complaint = (db_session.query(Complaint)
                 .filter(Complaint.complaint_id == body["complaint_id"])
                 .first()
                 )

    assert complaint is not None

def test_create_complaint_failure(client):
    customer = {"customer_id":"CUS001"}
    response = client.post("/complaints", json=customer)
    assert response.status_code == 422

def test_create_complaint_rollback(client, db_session, seeded_customer, monkeypatch):
    def fail(*args, **kwargs): raise Exception("boom")

    monkeypatch.setattr("data.repositories.complaint_status_history_repository.ComplaintStatusHistoryRepository.create", fail)

    complaintData = {
        "customer_id":"CUS001",
        "channel":"Email",
        "category":"SERVICE_DELAY",
        "complaint_text":"INTEGRATION ROLLBACK TEST",
        "status":"OPEN",
        "received_at":"2025-01-01T00:00:00"
    }

    response = client.post("/complaints", json = complaintData)

    complaint = (db_session.query(Complaint)
                 .filter(Complaint.complaint_text == "INTEGRATION ROLLBACK TEST")
                 .first()
                 )

    assert complaint is None




def test_valid_status_update(client, db_session, seeded_complaint):
    response = client.patch("/complaints/CMP001/status", params={"status":"In Progress"})

    assert response.status_code == 200

    complaint = (db_session.query(Complaint)
                 .filter(Complaint.complaint_id == "CMP001")
                 .first())
    
    assert complaint.status == ComplaintStatus.IN_PROGRESS

def test_invalid_status_update(client, seeded_complaint):
    response = client.patch("/complaints/CMP001/status", params={"status":"Closed"})
        
    assert response.status_code == 409




def test_safe_error_response(client):
    response = client.get("/customers/CUS999")

    body = response.json()

    assert "code" in body
    assert "message" in body

def test_correlation_id_present(client):
    response = client.get("/customers/CUS999")
    body = response.json()
    assert "X-Correlation-ID" in response.headers
    assert body["correlation_id"] is not None
