from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserBase, UserOut, UserCreateResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_current_user
from app.models.user import Users
from app.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create(user: UserBase, db:Session = Depends(get_db)):
    new_user = user_service.create_user(db, user)

    return {
        "message" : "user created",
        "data" : new_user
    }



@router.post("/login", status_code=200)
def login(payload: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    token = user_service.login_user(db,payload)

    return{
        "access_token" : token,
        "token_type" : "bearer"
    }



@router.get("/me", response_model = UserOut, status_code=200)
def get_user(db:Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return user_service.get_user_info(user, db)



@router.put("/me", response_model = UserCreateResponse, status_code=200)
def update_user(form_data:UserBase, db:Session = Depends(get_db), user: Users = Depends(get_current_user)):
    updated_user = user_service.update_user(user, form_data, db)

    return {
        "message" : "user updated",
        "data" : updated_user
    }



@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db:Session = Depends(get_db), user:Users = Depends(get_current_user)):
    return user_service.delete_user(db, user)