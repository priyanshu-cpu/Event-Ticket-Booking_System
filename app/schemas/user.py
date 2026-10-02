from pydantic import BaseModel, ConfigDict
from datetime import datetime



class UserBase(BaseModel):
    name: str
    email: str | None = None
    password: str



class UserOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    created_at: datetime



class UserCreateResponse(BaseModel):
    message: str
    data: UserOut


class UserLoginSchema(BaseModel):
    username: str
    password: str