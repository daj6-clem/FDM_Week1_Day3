from src.api.routers.complaints import get_by_id, get_complaints, get_csh_history, get_db, get_for_customer, create_complaint, change_status
from src.api.routers.customers import get_db, get_by_id, get_customers
from src.api.routers.health import live, ready
from fastapi import HTTPException
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

def test_complaint_get_by_id_success(client):
    response = client.get("/complaints/CMP001")
    assert response.status_code == 200
def test_complaint_get_by_id_fail(client):
    response = client.get("/complaints/CMP999")
    assert response.status_code == 404

def test_complaint_get_complaints(client):
    response = client.get("/complaints")
    assert response.status_code == 200

def test_complaint_get_for_customer_success(client):
    response = client.get("/customers/CUS001/complaints")
    assert response.status_code == 200
def test_complaint_get_for_customer_fail(client):
    response = client.get("customers/CUS999/complaints")
    assert response.status_code == 404

def test_complaint_create_complaint_success(client):
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

    response = client.post("/complaints",json = complaint)

    assert response.status_code == 201
    assert "complaint_id" in response.json()

def test_complaint_create_complaint_fail_validation(client):
    complaint = {
        "customer_id": "CUS001"
    }

    response = client.post("/complaints", json = complaint)

    assert response.status_code == 422

def test_complaint_create_complaint_fail_cus_dne(client):
    complaint = {
        "customer_id": "CUS999",
        "account_id": "ACC999",
        "channel": "Email",
        "category": "Service Delay",
        "complaint_text": "Test complaint",
        "priority": "Medium",
        "status": "Open",
        "received_at": datetime.now().isoformat(),
        "assigned_analyst_id": "EMP007"
    }

    response = client.post("/complaints", json = complaint)

    assert response.status_code in [400, 404, 500]

def test_complaint_change_status_success(client):
    response = client.patch("/complaints/CMP004/status",
                            params = {"status": "Closed"})
    assert response.status_code == 200
def test_complaint_change_status_fail_cmp_dne(client):
    response = client.patch("/complaints/CMP999/status",
                            params = {"status": "Under Review"})
    assert response.status_code == 404
def test_complaint_change_status_fail_invalid_trans(client):
    response = client.patch("/complaints/CMP001/status",
                            params = {"status": "Closed"})
    assert response.status_code == 409


def test_customer_get_by_id_fail(client):
    response = client.get(("/customers/CUS999"))
    assert response.status_code == 404
def test_customer_get_by_id_success(client):
    response = client.get("/customers/CUS001")
    assert response.status_code == 200
def test_customer_get_customers_success(client):
    response = client.get("/customers")
    assert response.status_code == 200

def test_health_live(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status":"alive"}

def test_health_ready(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {
            "status": "ready",
            "database": "connected"
        }
    