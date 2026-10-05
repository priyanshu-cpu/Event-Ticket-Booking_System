from fastapi import FastAPI
from app.api.routes.venue import router as venue_router
from app.api.routes.user import router as user_router
from app.api.routes.seat import router as seat_router
from app.api.routes.event import router as event_router




app = FastAPI()



app.include_router(venue_router)
app.include_router(user_router)
app.include_router(seat_router)
app.include_router(event_router)