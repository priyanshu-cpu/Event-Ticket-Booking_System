from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import event_repository
from app.models.event import Event
from app.schemas.event import EventBase, EventCreateResponse, EventOut




def create_event(data: EventBase, db:Session):
    return event_repository.create_event(data, db)
