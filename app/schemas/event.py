from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import EventStatus
from datetime import datetime



class EventBase(BaseModel):
    venue_id: int
    name : str = Field(min_length=1)
    description: str
    ticket_price: int

    
class EventCreate(EventBase):
    starts_at: datetime


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: EventStatus
    starts_at: datetime



class EventUpdate(BaseModel):
    name: str | None = None
    venue_id : int | None = None
    description: str | None = None
    ticket_price: int | None = None
    starts_at : datetime | None = None