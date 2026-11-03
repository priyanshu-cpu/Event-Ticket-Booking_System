from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.venue import VenueResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services import venue as venue_service



router = APIRouter(prefix="/api/venue", tags=["Venue"])


DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[VenueResponse])
async def get_venues(db:DbSession):
    return await venue_service.get_venues(db)
