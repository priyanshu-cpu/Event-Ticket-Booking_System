from app.repositories import venue as venue_repo
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool





async def get_venues(db:AsyncSession):
    return await venue_repo.get_venues(db)