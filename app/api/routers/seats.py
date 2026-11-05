from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.seats import Seat
from app.db.database import get_db
from app.schemas.seats import SeatResponse
from typing import Annotated
from app.services import seats as seat_service


router = APIRouter(prefix="/api/seats", tags=["Seats"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[SeatResponse])
async def get_seats(db:DbSession):
    return await seat_service.get_seats(db)