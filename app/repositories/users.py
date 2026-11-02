from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.user import User





async def email_exists(email:str, db:AsyncSession) -> bool:
    result = await db.scalar(select(exists().where(func.lower(User.email) == email.lower())))
    return result



async def get_by_email( email:str, db:AsyncSession) -> User | None:
    result = await db.scalar(select(User).where(func.lower(User.email) == email.lower()))
    return result


async def add_user( user:User, db:AsyncSession) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user