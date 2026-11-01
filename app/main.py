from fastapi import FastAPI
from app.api.routers.users import router as user_router




app = FastAPI(title="Event ticket booking system")

app.include_router(user_router)