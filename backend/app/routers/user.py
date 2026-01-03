"""
User router for profile and leaderboard.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.submission import Submission
from app.schemas.user import UserProfile, LeaderboardUser
from app.services.auth import get_current_user


router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile with stats.
    
    Returns user profile including rank and total submissions.
    """
    # Calculate user's rank based on total points
    rank_result = await db.execute(
        select(func.count(User.id))
        .where(User.total_points > current_user.total_points)
    )
    rank = rank_result.scalar() + 1
    
    # Get total submissions count
    submissions_result = await db.execute(
        select(func.count(Submission.id))
        .where(Submission.user_id == current_user.id)
    )
    total_submissions = submissions_result.scalar()
    
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak,
        total_points=current_user.total_points,
        last_completed_date=current_user.last_completed_date,
        created_at=current_user.created_at,
        rank=rank,
        total_submissions=total_submissions
    )


@router.get("/leaderboard", response_model=list[LeaderboardUser])
async def get_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get global leaderboard.
    
    Returns top users ranked by total points, then current streak.
    Limited to top 50 users by default.
    """
    # Get top users ordered by points, then streak
    result = await db.execute(
        select(User)
        .order_by(
            User.total_points.desc(),
            User.current_streak.desc(),
            User.longest_streak.desc()
        )
        .limit(limit)
    )
    users = result.scalars().all()
    
    # Build leaderboard with ranks
    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append(
            LeaderboardUser(
                rank=idx,
                id=user.id,
                username=user.username,
                total_points=user.total_points,
                current_streak=user.current_streak,
                longest_streak=user.longest_streak
            )
        )
    
    return leaderboard
