from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.seats import Seat
from app.db.database import get_db
from app.schemas.seats import SeatResponse
from typing import Annotated
from app.core.exceptions import NotFound
from app.services import seats as seat_service


router = APIRouter(prefix="/api/venue", tags=["Seats"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{venue_id}/seats", response_model=list[SeatResponse])
async def get_seats(venue_id:int, db:DbSession):
    try:
        seats = await seat_service.get_seats(venue_id, db)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return seats