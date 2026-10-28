from enum import Enum
import re

# ENUMS:
class Segment(Enum):
    RETAIL = "Retail"
    PREMIER = "Premier"
    BUSINESS = "Business"

class AccountType(Enum):
    CHEQUING = "Chequing"
    SAVINGS = "Savings"
    BUSINESS = "Business"

class AccountStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class ComplaintStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    UNDER_REVIEW = "Under Review"
    CLOSED = "Closed"

class Channel(Enum):
    PHONE = "Phone"
    EMAIL = "Email"
    BRANCH = "Branch"
    WEB = "Web"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Category(Enum):
    FEE_DISPUTE = "Fee Dispute"
    SERVICE_DELAY = "Service Delay"
    CARD_ISSUE = "Card Issue"
    CUSTOMER_SERVICE = "Customer Service"
    TRANSACTION_ERROR = "Transaction Error"
    ONLINE_BANKING = "Online Banking"
    FRAUD_CLAIM = "Fraud Claim"


class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone_number, segment, date_created):
        if not re.match(r"^CUS\d{3}$", customer_id):
            raise ValueError("Customer ID must be in the form CUS###")
        digits = ''.join(filter(str.isdigit, phone_number))
        if len(digits) != 10:
            raise ValueError("Phone number must contain 10 digits")
        if not isinstance(segment, Segment):
            raise ValueError("Invalid Segment")
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.segment = segment
        self.date_created = date_created

class Account:
    VALID_TRANSITIONS = {
        AccountStatus.ACTIVE: [AccountStatus.INACTIVE],
        AccountStatus.INACTIVE: [AccountStatus.ACTIVE]
    }

    def __init__(self, account_id, customer_id, account_number, account_type, status, current_balance, opened_date):
        if not re.match(r"^ACC\d{3}$", account_id):
            raise ValueError("Account ID must be in the form ACC###")
        if not isinstance(account_type, AccountType):
            raise ValueError("Invalid Account Type")
        if not isinstance(status, AccountStatus):
            raise ValueError("Invalid Account Status")
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.account_type = account_type
        self.status = status
        self.current_balance = current_balance
        self.opened_date = opened_date

    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise ValueError(f"Invalid transition: "
                             f"{self.status.value} -> {new_status.value}"
                             )
        self.status = new_status

class Complaint:
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


    def __init__(self, complaint_id, customer_id, account_id, channel, category, complaint_text, priority, status, received_at, assigned_analyst):
        if not re.match(r"^CMP\d{3}$", complaint_id):
            raise ValueError("Complaint ID must be in the form CMP###")
        if not isinstance(status, ComplaintStatus):
            raise ValueError("Invalid Complaint Status")
        if not isinstance(channel, Channel):
            raise ValueError("Invalid Complaint Channel")
        if not isinstance(priority, Priority):
            raise ValueError("Invalid Complaint Priority")
        if not isinstance(category, Category):
            raise ValueError("Invalid Complaint Category")
        if not complaint_text.strip():
            raise ValueError("Complaint Text Cannot Be Empty")
        
        self.complaint_id = complaint_id
        self.customer_id = customer_id
        self.account_id = account_id
        self.channel = channel
        self.category = category
        self.complaint_text = complaint_text
        self.priority = priority
        self.status = status
        self.received_at = received_at
        self.assigned_analyst = assigned_analyst

    def change_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise ValueError(f"Invalid transition: "
                             f"{self.status.value} -> {new_status.value}"
                             )
        self.status = new_status

class ComplaintStatusHistory:
    def __init__(self, history_id, complaint_id, old_status, new_status, changed_by, changed_at, comments):
        if old_status == new_status:
            raise ValueError("Old and New status cannot be the same")
        if not isinstance(old_status, ComplaintStatus):
            raise ValueError("Invalid Old Complaint Status")
        if not isinstance(new_status, ComplaintStatus):
            raise ValueError("Invalid New Complaint Status")
        self.history_id = history_id
        self.complaint_id = complaint_id
        self.old_status = old_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.changed_at = changed_at
        self.comments = comments