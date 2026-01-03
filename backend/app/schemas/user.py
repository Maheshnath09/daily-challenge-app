"""
User Pydantic schemas for request/response validation.
"""
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)."""
    id: UUID
    username: str
    email: str
    current_streak: int
    longest_streak: int
    total_points: int
    last_completed_date: date | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Schema for user profile with stats."""
    id: UUID
    username: str
    email: str
    current_streak: int
    longest_streak: int
    total_points: int
    last_completed_date: date | None
    created_at: datetime
    rank: int | None = None
    total_submissions: int = 0
    
    class Config:
        from_attributes = True


class LeaderboardUser(BaseModel):
    """Schema for leaderboard entry."""
    rank: int
    id: UUID
    username: str
    total_points: int
    current_streak: int
    longest_streak: int
    
    class Config:
        from_attributes = True
