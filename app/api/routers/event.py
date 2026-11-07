from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services import events as event_service
from app.core.exceptions import NotFound, Unauthorized
from app.models.user import User 
from app.utils.security import get_current_user



router = APIRouter(prefix="/api", tags=["events"])


DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/venue/{venue_id}/events", response_model=list[EventResponse])
async def get_events(venue_id:int, db:DbSession):
    try:
        events = await event_service.get_events(venue_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return events


@router.get("/event/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: int, db:DbSession):
    try:
        event = await event_service.get_event(event_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(event:EventCreate, db:DbSession, user:CurrentUser):
    try:
        result = await event_service.create_event(event, db, user)
    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to do this")
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found with this id")
    return result


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, db:DbSession, user: CurrentUser):
    try:
        result = await event_service.delete_event(event_id, db, user)
    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to do this")  
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found with this id")
    return result


@router.patch("/event_id", response_model=EventResponse)
async def update_event(event_id: int, event_data: EventUpdate, db:DbSession, user: CurrentUser):
    try:
        result = await event_service.update_event(event_id, event_data, db, user)
    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to do this")  