from data.base import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import relationship
from src.api.error_handlers.error_handlers import InvalidStatusTransitionException
import datetime
import uuid
from sqlalchemy import JSON

# ENUMS:
class Segment(Enum):
    Retail = "Retail"
    Premier = "Premier"
    Business = "Business"

class AccountType(Enum):
    Chequing = "Chequing"
    Savings = "Savings"
    Business = "Business"

class AccountStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class ComplaintStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    UNDER_REVIEW = "Under Review"
    CLOSED = "Closed"

class Channel(Enum):
    Phone = "Phone"
    Email = "Email"
    Branch = "Branch"
    Web = "Web"

class Priority(Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"

class Category(Enum):
    FEE_DISPUTE = "Fee Dispute"
    SERVICE_DELAY = "Service Delay"
    CARD_ISSUE = "Card Issue"
    CUSTOMER_SERVICE = "Customer Service"
    TRANSACTION_ERROR = "Transaction Error"
    ONLINE_BANKING = "Online Banking"
    FRAUD_CLAIM = "Fraud Claim"

class ApprovalStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class Customer (Base):
    __tablename__ = "customer"

    customer_id = Column(String, primary_key = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True)
    phone_number = Column(String, nullable = True)
    segment = Column(SqlEnum(Segment), nullable = True)
    date_created = Column(DateTime, default = datetime.datetime.utcnow, nullable = True)

class Account (Base):
    __tablename__ = "account"

    account_id = Column(String, primary_key = True)
    customer_id = Column(String, ForeignKey("customer.customer_id"), nullable = False)
    account_number = Column(String, unique = True, nullable = False)
    account_type = Column(SqlEnum(AccountType), nullable = False)
    status = Column(SqlEnum(AccountStatus), nullable = False)
    current_balance = Column(Float, default = 0, nullable = True)
    opened_date = Column(DateTime, nullable = False)

    VALID_TRANSITIONS = {
    AccountStatus.ACTIVE: [AccountStatus.INACTIVE],
    AccountStatus.INACTIVE: [AccountStatus.ACTIVE]
    }

    # Function tested
    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise ValueError(f"Invalid transition: "
                             f"{self.status.value} -> {new_status.value}"
                             )
        self.status = new_status

class Complaint (Base):
    __tablename__ = "complaint"

    complaint_id = Column(String, primary_key = True)
    customer_id = Column(String, ForeignKey("customer.customer_id"), nullable = False)
    account_id = Column(String, ForeignKey("account.account_id"), nullable = True)
    channel = Column(SqlEnum(Channel), nullable = False)
    category = Column(SqlEnum(Category, values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable = False)
    complaint_text = Column(String, nullable = False)
    priority = Column(SqlEnum(Priority), nullable = True)
    status = Column(SqlEnum(ComplaintStatus), nullable = False)
    received_at = Column(DateTime, nullable = False)
    assigned_analyst_id = Column(String, ForeignKey("employee.employee_id"), nullable = True)


    notes = relationship("ComplaintNote", back_populates="complaint")

    review_requests = relationship("ReviewRequest", back_populates="complaint")
    VALID_TRANSITIONS = {
        ComplaintStatus.OPEN: [
            ComplaintStatus.IN_PROGRESS
        ],
        ComplaintStatus.IN_PROGRESS: [
            ComplaintStatus.UNDER_REVIEW,
            ComplaintStatus.CLOSED
        ],
        ComplaintStatus.UNDER_REVIEW: [
            ComplaintStatus.CLOSED
        ],
        ComplaintStatus.CLOSED: []
    }

    # Function Tested
    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise InvalidStatusTransitionException(f"Invalid transition: "
                             f"{self.status.value} -> {new_status.value}"
                             )
        self.status = new_status

class ComplaintStatusHistory (Base):
    __tablename__ = "complaint_status_history"

    history_id = Column(Integer, primary_key = True, autoincrement=True)
    complaint_id = Column(String, ForeignKey("complaint.complaint_id"), nullable = False)
    old_status = Column(SqlEnum(ComplaintStatus), nullable = True)
    new_status = Column(SqlEnum(ComplaintStatus), nullable = False)
    changed_by = Column(String, ForeignKey("employee.employee_id"), nullable = True)
    changed_at = Column(DateTime, default = datetime.datetime.utcnow, nullable = True)
    comments = Column(String, nullable = True)

class Employee (Base):
    __tablename__ = "employee"

    employee_id = Column(String, primary_key = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True)
    role = Column(String, nullable = False)

class ComplaintNote(Base):
    __tablename__="complaint_notes"

    note_id = Column(String, primary_key = True, default = lambda:str(uuid.uuid4()))
    complaint_id = Column(String, ForeignKey("complaint.complaint_id"), nullable = False)
    note_text = Column(String, nullable = False)
    evidence_refs = Column(JSON, nullable = True)
    created_at = Column(DateTime, default = datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="notes")

class ReviewRequest(Base):
    __tablename__="review_request"

    review_request_id = Column(String, primary_key=True)
    complaint_id = Column(String, ForeignKey("complaint.complaint_id"), nullable=False)
    recommendation_id = Column(String, ForeignKey("recommendation.recommendation_id"), nullable = False)
    reviewer_id = Column(String, ForeignKey("employee.employee_id"), nullable = False)
    requested_at = Column(DateTime,default=datetime.datetime.utcnow)
    status = Column(SqlEnum(ApprovalStatus))

    complaint = relationship(
        "Complaint",
        back_populates="review_requests"
    )

    decisions = relationship(
        "ReviewDecision",
        back_populates="review_request"
    )

    VALID_TRANSITIONS = {
        ApprovalStatus.PENDING: [
            ApprovalStatus.APPROVED,
            ApprovalStatus.REJECTED
        ],
        ApprovalStatus.APPROVED: [],
        ApprovalStatus.REJECTED: []
    }

    # Function Tested
    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise InvalidStatusTransitionException(f"Invalid transition: "
                             f"{self.status.value} -> {new_status.value}"
                             )
        self.status = new_status

class ReviewDecision(Base):
    __tablename__ = "review_decision"

    decision_id = Column(String, primary_key = True)
    review_request_id = Column(String, ForeignKey("review_request.review_request_id"), nullable = False)
    decision = Column(String)
    decision_reason = Column(String)
    decision_date = Column(DateTime, default = datetime.datetime.utcnow)

    review_request = relationship(
        "ReviewRequest",
        back_populates="decisions"
    )

class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_id = Column(String,primary_key=True,default=lambda: str(uuid.uuid4()))
    entity_name = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    action_type = Column(String, nullable = False)
    performed_by = Column(String, nullable = True)
    event_timestamp = Column(DateTime, default = datetime.datetime.utcnow)
    details = Column(String)



# Investigation_id should be a foreign key, change this back once you're done with tool implementation

class Recommendation(Base):
    __tablename__ = "recommendation"

    recommendation_id = Column(String, primary_key = True)
    investigation_id = Column(String)
    recommendation_text = Column(String)
    confidence_score = Column(Float)
    generated_at = Column(DateTime, default = datetime.datetime.utcnow)