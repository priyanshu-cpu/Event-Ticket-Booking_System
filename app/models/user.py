from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, ForeignKey
from app.db.database import Base
from datetime import datetime, UTC


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash:Mapped[str] = mapped_column(nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

