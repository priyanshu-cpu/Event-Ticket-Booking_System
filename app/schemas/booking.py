from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BookingBase(BaseModel):
    event_id : int
    seat_id: int



class BookingOut(BaseModel):
    id: int
    user_id: int
    event_id : int
    seat_id: int
    status: str
    hold_expires_at: datetime|None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingCreatedResponse(BaseModel):
    message: str
    data: BookingOut