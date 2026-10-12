
def get_seat_hold_key(event_id: int, seat_id: int) -> str:
    return f"seat_hold:event:{event_id}:seat:{seat_id}"