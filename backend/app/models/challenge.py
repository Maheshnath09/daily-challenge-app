"""
Challenge model for daily challenges.
"""
import uuid
from datetime import datetime, date
from enum import Enum as PyEnum
from sqlalchemy import String, Text, Date, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ChallengeCategory(str, PyEnum):
    """Challenge category types."""
    LOGIC = "logic"
    CODING = "coding"
    LIFE = "life"


class ChallengeDifficulty(str, PyEnum):
    """Challenge difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Challenge(Base):
    """Challenge model for daily challenges."""
    
    __tablename__ = "challenges"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    category: Mapped[ChallengeCategory] = mapped_column(
        Enum(ChallengeCategory),
        nullable=False
    )
    difficulty: Mapped[ChallengeDifficulty] = mapped_column(
        Enum(ChallengeDifficulty),
        nullable=False
    )
    expected_output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    # Date control
    active_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
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
        back_populates="challenge",
        lazy="selectin"
    )
    
    def get_points(self) -> int:
        """Get base points for this challenge difficulty."""
        points_map = {
            ChallengeDifficulty.EASY: 10,
            ChallengeDifficulty.MEDIUM: 20,
            ChallengeDifficulty.HARD: 30,
        }
        return points_map.get(self.difficulty, 10)
    
    def __repr__(self) -> str:
        return f"<Challenge {self.title} ({self.active_date})>"
