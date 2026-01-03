"""
Challenge Pydantic schemas for request/response validation.
"""
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.challenge import ChallengeCategory, ChallengeDifficulty


class ChallengeCreate(BaseModel):
    """Schema for creating a challenge."""
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    expected_output: str | None = None
    active_date: date


class ChallengeResponse(BaseModel):
    """Schema for challenge response."""
    id: UUID
    title: str
    description: str
    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    expected_output: str | None
    active_date: date
    is_active: bool
    created_at: datetime
    points: int = 0
    user_submitted: bool = False
    
    class Config:
        from_attributes = True


class ChallengeHistory(BaseModel):
    """Schema for challenge history list."""
    challenges: list[ChallengeResponse]
    total: int
    page: int
    page_size: int
