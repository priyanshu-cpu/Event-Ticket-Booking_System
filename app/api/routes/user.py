from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserBase, UserOut, UserCreateResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.services import user_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create(user: UserBase, db:Session = Depends(get_db)):
    new_user = user_service.create_user(db, user)

    return {
        "message" : "user created",
        "data" : new_user
    }



@router.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    token = user_service.login_user(db,payload)

    return{
        "access_token" : token,
        "token_type" : "bearer"
    }


