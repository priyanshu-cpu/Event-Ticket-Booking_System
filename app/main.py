from fastapi import FastAPI
from app.api.routers.users import router as user_router
from app.api.routers.venue import router as venue_router




app = FastAPI(title="Event ticket booking system")

app.include_router(user_router)
app.include_router(venue_router)