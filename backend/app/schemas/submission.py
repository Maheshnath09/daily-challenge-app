"""
Submission Pydantic schemas for request/response validation.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.submission import SubmissionType


class SubmissionCreate(BaseModel):
    """Schema for creating a submission."""
    challenge_id: UUID
    content: str | None = Field(None, max_length=10000)
    submission_type: SubmissionType = SubmissionType.TEXT
    completed: bool = True


class SubmissionResponse(BaseModel):
    """Schema for submission response."""
    id: UUID
    user_id: UUID
    challenge_id: UUID
    content: str | None
    submission_type: str
    completed: bool
    points_awarded: int
    submitted_at: datetime
    
    class Config:
        from_attributes = True
