"""
Challenge router for daily challenge operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.challenge import ChallengeResponse, ChallengeHistory
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.services.auth import get_current_user
from app.services.challenge import (
    get_today_challenge,
    get_challenge_history,
    get_challenge_by_id,
    check_user_submitted
)
from app.services.submission import create_submission


router = APIRouter(prefix="/challenge", tags=["Challenges"])


@router.get("/today", response_model=ChallengeResponse)
async def get_todays_challenge(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get today's active challenge.
    
    Returns the current day's challenge with submission status.
    """
    challenge = await get_today_challenge(db)
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No challenge available for today"
        )
    
    # Check if user has submitted
    user_submitted = await check_user_submitted(db, current_user.id, challenge.id)
    
    return ChallengeResponse(
        id=challenge.id,
        title=challenge.title,
        description=challenge.description,
        category=challenge.category,
        difficulty=challenge.difficulty,
        expected_output=challenge.expected_output,
        active_date=challenge.active_date,
        is_active=challenge.is_active,
        created_at=challenge.created_at,
        points=challenge.get_points(),
        user_submitted=user_submitted
    )


@router.get("/history", response_model=ChallengeHistory)
async def get_challenges_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get past challenges history.
    
    Returns paginated list of past challenges with submission status.
    """
    challenges, total = await get_challenge_history(db, current_user.id, page, page_size)
    
    challenge_responses = []
    for challenge in challenges:
        user_submitted = await check_user_submitted(db, current_user.id, challenge.id)
        challenge_responses.append(
            ChallengeResponse(
                id=challenge.id,
                title=challenge.title,
                description=challenge.description,
                category=challenge.category,
                difficulty=challenge.difficulty,
                expected_output=challenge.expected_output,
                active_date=challenge.active_date,
                is_active=challenge.is_active,
                created_at=challenge.created_at,
                points=challenge.get_points(),
                user_submitted=user_submitted
            )
        )
    
    return ChallengeHistory(
        challenges=challenge_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_challenge(
    submission_data: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit an answer for today's challenge.
    
    - Only one submission per challenge allowed
    - Late submissions are rejected
    - Streak and points are calculated server-side
    """
    # Get the challenge
    challenge = await get_challenge_by_id(db, submission_data.challenge_id)
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    try:
        submission = await create_submission(
            db=db,
            user=current_user,
            challenge=challenge,
            submission_data=submission_data
        )
        return submission
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
