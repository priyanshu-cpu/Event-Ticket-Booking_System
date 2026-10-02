from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserBase, UserOut, UserCreateResponse

from app.services import user_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserCreateResponse)
def create(user: UserBase, db:Session = Depends(get_db)):
    new_user = user_service.create_user(db, user)

    return {
        "message" : "user created",
        "data" : new_user
    }