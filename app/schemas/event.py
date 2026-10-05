from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime


class EventBase(BaseModel):
    venue_id: int
    name:str
    description: str | None = None
    event_date: date
    start_time: time
    end_time: time
    ticket_price: int



class EventOut(BaseModel):
    id: int
    venue_id: int
    name:str
    description: str | None = None
    event_date: date
    start_time: time
    end_time: time
    ticket_price: int
    created_at: datetime



class EventCreateResponse(BaseModel):
    message : str
    data: EventOut
    