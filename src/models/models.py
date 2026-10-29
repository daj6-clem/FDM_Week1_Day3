from data.base import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import relationship
import datetime

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

    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise ValueError(f"Invalid transition: "
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