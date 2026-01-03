"""
Challenge service for managing daily challenges.
"""
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.challenge import Challenge
from app.models.submission import Submission
from app.schemas.challenge import ChallengeCreate


async def get_today_challenge(db: AsyncSession) -> Optional[Challenge]:
    """
    Get today's active challenge.
    
    Args:
        db: Database session
    
    Returns:
        Today's challenge or None if not found
    """
    today = date.today()
    
    result = await db.execute(
        select(Challenge).where(
            and_(
                Challenge.active_date == today,
                Challenge.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()


async def get_challenge_by_id(
    db: AsyncSession,
    challenge_id: UUID
) -> Optional[Challenge]:
    """
    Get a challenge by its ID.
    
    Args:
        db: Database session
        challenge_id: Challenge UUID
    
    Returns:
        Challenge or None if not found
    """
    result = await db.execute(
        select(Challenge).where(Challenge.id == challenge_id)
    )
    return result.scalar_one_or_none()


async def get_challenge_history(
    db: AsyncSession,
    user_id: UUID,
    page: int = 1,
    page_size: int = 10
) -> tuple[list[Challenge], int]:
    """
    Get past challenges with user submission status.
    
    Args:
        db: Database session
        user_id: Current user's UUID
        page: Page number
        page_size: Number of items per page
    
    Returns:
        Tuple of (challenges list, total count)
    """
    today = date.today()
    offset = (page - 1) * page_size
    
    # Get total count
    count_result = await db.execute(
        select(Challenge).where(Challenge.active_date < today)
    )
    total = len(count_result.scalars().all())
    
    # Get paginated challenges
    result = await db.execute(
        select(Challenge)
        .where(Challenge.active_date < today)
        .order_by(Challenge.active_date.desc())
        .offset(offset)
        .limit(page_size)
    )
    challenges = result.scalars().all()
    
    return list(challenges), total


async def create_challenge(
    db: AsyncSession,
    challenge_data: ChallengeCreate
) -> Challenge:
    """
    Create a new challenge.
    
    Args:
        db: Database session
        challenge_data: Challenge creation data
    
    Returns:
        Created challenge
    """
    challenge = Challenge(
        title=challenge_data.title,
        description=challenge_data.description,
        category=challenge_data.category,
        difficulty=challenge_data.difficulty,
        expected_output=challenge_data.expected_output,
        active_date=challenge_data.active_date,
        is_active=challenge_data.active_date == date.today()
    )
    
    db.add(challenge)
    await db.flush()
    await db.refresh(challenge)
    
    return challenge


async def activate_today_challenge(db: AsyncSession) -> Optional[Challenge]:
    """
    Activate today's challenge and deactivate others.
    Called by the scheduler at midnight UTC.
    
    Args:
        db: Database session
    
    Returns:
        Activated challenge or None
    """
    today = date.today()
    
    # Deactivate all challenges
    all_challenges_result = await db.execute(select(Challenge))
    all_challenges = all_challenges_result.scalars().all()
    
    for challenge in all_challenges:
        challenge.is_active = False
    
    # Activate today's challenge
    result = await db.execute(
        select(Challenge).where(Challenge.active_date == today)
    )
    today_challenge = result.scalar_one_or_none()
    
    if today_challenge:
        today_challenge.is_active = True
    
    await db.commit()
    
    return today_challenge


async def check_user_submitted(
    db: AsyncSession,
    user_id: UUID,
    challenge_id: UUID
) -> bool:
    """
    Check if user has already submitted for a challenge.
    
    Args:
        db: Database session
        user_id: User's UUID
        challenge_id: Challenge's UUID
    
    Returns:
        True if user has submitted, False otherwise
    """
    result = await db.execute(
        select(Submission).where(
            and_(
                Submission.user_id == user_id,
                Submission.challenge_id == challenge_id
            )
        )
    )
    return result.scalar_one_or_none() is not None
