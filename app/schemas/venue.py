from pydantic import BaseModel, ConfigDict, Field


class VenueBase(BaseModel):
    name : str = Field(min_length=5)
    location: str = Field(min_length=5)


class VenueCreate(VenueBase):
    pass


class VenueResponse(VenueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
