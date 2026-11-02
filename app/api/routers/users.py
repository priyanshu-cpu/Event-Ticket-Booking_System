from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserResponse, UserCreate, Token
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import EmailAlreadyExists, InvalidCredentials
from app.services import users as user_service
from app.db.database import get_db
from app.utils.security import get_current_user



DbSession = Annotated[AsyncSession, Depends(get_db)]



router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db:DbSession):
    try:
        return await user_service.add_user(user, db)
    except EmailAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")



@router.post("/token", response_model=Token)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:DbSession):
    try:
        result = await user_service.login_user(form_data, db)
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return Token(access_token=result, token_type="bearer")
    

@router.get("/me", response_model=UserResponse)
async def me(user: Annotated[User, Depends(get_current_user)]):
    return user