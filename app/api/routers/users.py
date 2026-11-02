from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from app.schemas.users import UserCreate, UserResponse, Token
from app.models.user import User
from app.db.database import get_db
from app.utils.security import generate_password_hash, verify_password, get_current_user, create_token, DUMMY_HASH

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    db_user = await db.scalar(select(User.id).where(func.lower(User.email) == user.email.lower()))
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    password_hash = await run_in_threadpool(generate_password_hash, user.password)
    new_user = User(
        email=user.email.lower(), password_hash=password_hash
    )

    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    await db.refresh(new_user)

    return new_user



@router.post("/token", response_model=Token)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
    user = await db.scalar(select(User).where(User.email == form_data.username))
    
    password_hash = user.password_hash if user else DUMMY_HASH

    valid = await run_in_threadpool(verify_password, form_data.password, password_hash)

    if not user or not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_token(data={"sub" : str(user.id)})

    return Token(
        access_token= token,
        token_type="bearer"
    )



@router.get("/me", response_model=UserResponse)
async def me(user: Annotated[User, Depends(get_current_user)]):
    return user