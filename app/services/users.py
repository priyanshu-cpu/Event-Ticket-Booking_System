from app.repositories import users as user_repo
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool
from app.models.user import User
from app.schemas.users import UserCreate
from app.core.exceptions import EmailAlreadyExists
from app.utils.security import generate_password_hash, verify_password, create_token, get_current_user




async def add_user(data:UserCreate, db:AsyncSession) -> User:
    email = data.email.lower()
    if await user_repo.email_exists(email, db):
        raise EmailAlreadyExists(email)

    password_hash = await run_in_threadpool(generate_password_hash, data.password)

    try:
        user = await user_repo.add_user(User(email = data.email, password_hash = password_hash), db)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise EmailAlreadyExists(email)
    return user