from pydantic import BaseModel
from datetime import datetime
from src.models.models import Segment, Channel, Category, Priority, ComplaintStatus
##WIP

#This includes everything but the id
class CustomerCreate(BaseModel):
    first_name:str
    last_name:str
    email: str
    phone_number:str | None
    segment: Segment | None
    date_created: datetime | None


#This includes everything and the id
class CustomerResponse(BaseModel):
    customer_id:str
    first_name:str
    last_name:str
    email: str
    phone_number:str | None
    segment: Segment | None
    date_created: datetime | None

class ComplaintCreate(BaseModel):
    customer_id:str
    account_id:str | None
    channel:Channel
    category:Category
    complaint_text:str
    priority:Priority | None
    status:ComplaintStatus
    received_at:datetime
    assigned_analyst_id:str | None

class ComplaintResponse(BaseModel):
    complaint_id:str
    customer_id:str
    account_id:str | None
    channel:Channel
    category:Category
    complaint_text:str
    priority:Priority | None
    status:ComplaintStatus
    received_at:datetime
    assigned_analyst_id:str | None

class ComplaintStatusHistoryCreate(BaseModel):
    complaint_id:str
    old_status:ComplaintStatus | None
    new_status:ComplaintStatus
    changed_by:str | None
    changed_at:datetime | None
    comments:str | None