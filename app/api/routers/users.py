from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from app.schemas.users import UserCreate, UserResponse, UserLogin
from app.models.user import User
from app.db.database import get_db
from app.utils.security import generate_password_hash, verify_password, get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    db_user = await db.scalar(select(User.id).where(func.lower(User.email) == user.email))
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
