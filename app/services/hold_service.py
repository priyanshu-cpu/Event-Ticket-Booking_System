from app.redis.client import redis_client
from app.redis.keys import get_seat_hold_key


HOLD_DURATION = 300


async def hold_seat(event_id: int, seat_id: int, user_id: int):
    key = get_seat_hold_key(event_id, seat_id)

    result = await redis_client.set(
        key,
        user_id,
        nx=True,
        ex=HOLD_DURATION
    )

    return bool(result)

async def check_seat_hold(event_id: int, seat_id: int):
    key = get_seat_hold_key(event_id, seat_id)
    return await redis_client.get(key)

