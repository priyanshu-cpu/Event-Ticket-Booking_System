from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import BookingStatus
from datetime import datetime


class BookingBase(BaseModel):
    event_id: int
    seat_id: int


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: BookingStatus
    created_at: datetime | None = None