from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.event import EventCreate, EventResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services import events as event_service
from app.core.exceptions import NotFound



router = APIRouter("/api/venue", tags=["events"])


DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{venue_id}/events", response_model=list[EventResponse])
async def get_events(venue_id:int, db:DbSession):
    try:
        events = await event_service.get_events(venue_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: int, db:DbSession):
    try:
        event = event_service.get_event(event_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return event