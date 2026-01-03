"""
Submission service with streak and points logic.
CRITICAL: All streak logic is server-side only.
"""
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.user import User
from app.models.challenge import Challenge
from app.models.submission import Submission, SubmissionType
from app.schemas.submission import SubmissionCreate


# Points configuration
POINTS_MAP = {
    "easy": 10,
    "medium": 20,
    "hard": 30,
}
STREAK_BONUS = 5
STREAK_BONUS_THRESHOLD = 7


def calculate_points(difficulty: str, current_streak: int) -> int:
    """
    Calculate points for a submission.
    
    Args:
        difficulty: Challenge difficulty level
        current_streak: User's current streak (after this submission)
    
    Returns:
        Total points to award
    """
    base_points = POINTS_MAP.get(difficulty.lower(), 10)
    
    # Add streak bonus if streak is 7+ days
    if current_streak >= STREAK_BONUS_THRESHOLD:
        return base_points + STREAK_BONUS
    
    return base_points


def update_streak(
    user: User,
    submission_date: date
) -> int:
    """
    Update user's streak based on submission date.
    
    CRITICAL STREAK LOGIC:
    - Streak increments only if challenge completed before midnight
    - If user completed yesterday's challenge, streak continues
    - If a day is skipped, streak resets to 1 (this is a new start)
    - Longest streak is preserved forever
    
    Args:
        user: User model instance
        submission_date: Date of submission
    
    Returns:
        New current streak value
    """
    today = submission_date
    
    if user.last_completed_date is None:
        # First ever submission
        user.current_streak = 1
    elif user.last_completed_date == today - timedelta(days=1):
        # Consecutive day - increment streak
        user.current_streak += 1
    elif user.last_completed_date == today:
        # Same day submission - no change to streak
        # This shouldn't happen due to unique constraint, but handle gracefully
        pass
    else:
        # Streak broken (skipped one or more days) - reset to 1
        user.current_streak = 1
    
    # Update longest streak if current exceeds it
    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak
    
    # Update last completed date
    user.last_completed_date = today
    
    return user.current_streak


async def create_submission(
    db: AsyncSession,
    user: User,
    challenge: Challenge,
    submission_data: SubmissionCreate
) -> Submission:
    """
    Create a new submission and update user stats.
    
    Args:
        db: Database session
        user: Submitting user
        challenge: Challenge being submitted for
        submission_data: Submission data
    
    Returns:
        Created submission
    
    Raises:
        ValueError: If challenge is not active or user already submitted
    """
    today = date.today()
    
    # Validate challenge is today's challenge and active
    if challenge.active_date != today:
        raise ValueError("Cannot submit for past or future challenges")
    
    if not challenge.is_active:
        raise ValueError("Challenge is not active")
    
    # Check if user already submitted
    existing = await db.execute(
        select(Submission).where(
            and_(
                Submission.user_id == user.id,
                Submission.challenge_id == challenge.id
            )
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("You have already submitted for this challenge")
    
    # Update streak
    new_streak = update_streak(user, today)
    
    # Calculate points
    points = calculate_points(challenge.difficulty.value, new_streak)
    
    # Update user's total points
    user.total_points += points
    
    # Create submission
    submission = Submission(
        user_id=user.id,
        challenge_id=challenge.id,
        content=submission_data.content,
        submission_type=submission_data.submission_type.value,
        completed=submission_data.completed,
        points_awarded=points,
        submitted_at=datetime.utcnow()
    )
    
    db.add(submission)
    await db.flush()
    await db.refresh(submission)
    
    return submission


async def get_user_submission(
    db: AsyncSession,
    user_id: UUID,
    challenge_id: UUID
) -> Optional[Submission]:
    """
    Get a user's submission for a specific challenge.
    
    Args:
        db: Database session
        user_id: User's UUID
        challenge_id: Challenge's UUID
    
    Returns:
        Submission or None if not found
    """
    result = await db.execute(
        select(Submission).where(
            and_(
                Submission.user_id == user_id,
                Submission.challenge_id == challenge_id
            )
        )
    )
    return result.scalar_one_or_none()


async def get_user_submissions(
    db: AsyncSession,
    user_id: UUID,
    limit: int = 50
) -> list[Submission]:
    """
    Get a user's recent submissions.
    
    Args:
        db: Database session
        user_id: User's UUID
        limit: Maximum number of submissions to return
    
    Returns:
        List of submissions
    """
    result = await db.execute(
        select(Submission)
        .where(Submission.user_id == user_id)
        .order_by(Submission.submitted_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
