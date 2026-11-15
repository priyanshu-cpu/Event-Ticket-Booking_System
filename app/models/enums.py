import enum


class EventStatus(str, enum.Enum):
    draft = "draft"
    published = "published"

class BookingStatus(str, enum.Enum):
    pending = "pending"
    held = "held"
    confirmed = "confirmed"
    expired = "expired"