import redis
from app.core.config import settings


redis_client = redis.Redis(
    settings.REDIS_URL,
    decode_responses=True
)