from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.venue import VenueResponse, VenueCreate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services import venue as venue_service
from app.core.exceptions import NotFound, VenueAlreadyExists, Unauthorized
from app.utils.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/api/venue", tags=["Venue"])


DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[VenueResponse])
async def get_venues(db:DbSession):
    return await venue_service.get_venues(db)


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(venue_id: int, db:DbSession):
    try:
        venue = await venue_service.get_venue(venue_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return venue


@router.post("", response_model=VenueResponse, status_code=201)
async def create_venue(venue_data: VenueCreate, db:DbSession, user: CurrentUser):
    try:
        result = await venue_service.create_venue(venue_data, user, db)
    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to do this.")
    except VenueAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Venue already exists")

    return result


@router.delete("/{venue_id}", status_code=204)
async def delete_venue(venue_id: int, db:DbSession, user: CurrentUser):
    try:
        result = await venue_service.delete_venue(venue_id, db, user)
    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to do this.")
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return result