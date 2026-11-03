from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from data.base import Base
from datetime import datetime
from src.models.models import Customer, Complaint, ComplaintStatus, Channel, Category
from src.api.main import app
from src.dependencies import get_db

import pytest

TEST_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)

    yield
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def seeded_customer(db_session):
    customer = Customer(
        customer_id="CUS001",
        first_name="Test",
        last_name="Customer",
        email="test@test.com",
        date_created=datetime(2025, 1, 1)
    )

    db_session.add(customer)
    db_session.commit()

    return customer

@pytest.fixture
def seeded_complaint(db_session, seeded_customer):
    complaint = Complaint(
        complaint_id="CMP001",
        customer_id="CUS001",
        channel = Channel.Email,
        category = Category.SERVICE_DELAY,
        complaint_text = "Test",
        status = ComplaintStatus.OPEN,
        received_at = datetime(2025, 1, 1)
    )

    db_session.add(complaint)
    db_session.commit()

    return complaint

@pytest.fixture
def client(db_session):
    
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()