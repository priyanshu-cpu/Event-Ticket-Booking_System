from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email : EmailStr = Field(max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=50)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id : int
    created_at: datetime



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"