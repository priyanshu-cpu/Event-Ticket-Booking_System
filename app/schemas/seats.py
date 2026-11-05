from pydantic import BaseModel, ConfigDict, Field

class SeatBase(BaseModel):
    row: str = Field(min_length=1)
    seat_number: int = Field(ge=1, le=10)


class SeatResponse(SeatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int