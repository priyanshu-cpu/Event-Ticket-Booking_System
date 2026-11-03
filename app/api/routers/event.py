from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.event import EventCreate, EventResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
# from app.services import 



router = APIRouter("/api/venue", tags=["events"])


@router.get("/events", response_model=list[EventResponse])
async def get_events():
    pass