from pydantic import BaseModel, ConfigDict


class SeatBase(BaseModel):

    venue_id: int
    row: str
    seat_no : int


class SeatOut(BaseModel):
    id: int
    venue_id: int
    row: str
    seat_no : int

    model_config = ConfigDict(from_attributes=True)

class SeatCreatResponse(BaseModel):
    message: str
    data: SeatOut

    