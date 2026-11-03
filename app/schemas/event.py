from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import EventStatus
from datetime import datetime, UTC



class EventBase(BaseModel):
    venue_id: int
    name : str = Field(min_length=1)


class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: EventStatus
    starts_at: datetime
