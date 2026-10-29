from pydantic import BaseModel
from sqlalchemy import DateTime
from src.models.models import Segment
##WIP

#This includes everything but the id
class CustomerCreate(BaseModel):
    first_name:str
    last_name:str
    email: str
    phone_number:str | None
    segment: Segment | None
    date_created: DateTime | None


#This includes everything and the id
class CustomerResponse(BaseModel):
    customer_id:str
    first_name:str
    last_name:str
    email: str
    phone_number:str | None
    segment: Segment | None
    date_created: DateTime | None