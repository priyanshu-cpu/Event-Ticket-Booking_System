from pydantic import BaseModel, ConfigDict


class SeatBase(BaseModel):

    venue_id: int
    row: str
    seat_number : int


class SeatOut(BaseModel):
    id: int
    row: str
    seat_number : int

    model_config = ConfigDict(from_attributes=True)

class SeatCreatResponse(BaseModel):
    message: str
    data: SeatOut

    