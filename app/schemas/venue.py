from pydantic import BaseModel, ConfigDict


class VenueCreate(BaseModel):
    name: str
    location: str



class VenueOut(BaseModel):
    id: int
    name: str
    location: str

    model_config = ConfigDict(from_attributes=True)

class VenueCreateResponse(BaseModel):
    message: str
    data: VenueOut