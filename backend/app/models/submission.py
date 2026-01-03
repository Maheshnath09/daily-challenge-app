"""
Submission model for user challenge submissions.
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from app.database import Base


class SubmissionType(str, PyEnum):
    """Submission types."""
    TEXT = "text"
    CODE = "code"
    CHECKBOX = "checkbox"


class Submission(Base):
    """Submission model for user answers to challenges."""
    
    __tablename__ = "submissions"
    
    # Add unique constraint for user_id + challenge_id
    __table_args__ = (
        UniqueConstraint('user_id', 'challenge_id', name='unique_user_challenge_submission'),
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("challenges.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Submission content
    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    submission_type: Mapped[str] = mapped_column(
        String(20),
        default=SubmissionType.TEXT.value,
        nullable=False
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    # Points awarded
    points_awarded: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    
    # Timestamps
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="submissions"
    )
    challenge: Mapped["Challenge"] = relationship(
        "Challenge",
        back_populates="submissions"
    )
    
    def __repr__(self) -> str:
        return f"<Submission {self.user_id} -> {self.challenge_id}>"
