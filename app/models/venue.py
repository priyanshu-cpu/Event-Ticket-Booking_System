from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base



class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    