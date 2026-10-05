from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Annotated



class UserBase(BaseModel):
    name: str
    email: str | None = None
    password: str



class UserOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class UserCreateResponse(BaseModel):
    message: str
    data: UserOut



class UserLoginSchema(BaseModel):
    username: str
    password: str