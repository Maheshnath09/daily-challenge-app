"""
User model for authentication and profile data.
"""
import uuid
from datetime import datetime, date
from sqlalchemy import String, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class User(Base):
    """User model storing authentication and streak/points data."""
    
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    # Streak tracking
    current_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    longest_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_points: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    last_completed_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="user",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
