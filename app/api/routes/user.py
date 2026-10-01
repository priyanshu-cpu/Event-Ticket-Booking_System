from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserBase, UserOut, UserCreateResponse



router = APIRouter(prefix="/auth", tags=["Auth"])