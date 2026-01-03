"""
Scheduler service for daily background tasks.
Uses APScheduler to run jobs at midnight UTC.
"""
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database import AsyncSessionLocal
from app.services.challenge import activate_today_challenge

# Configure logging
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def daily_challenge_rotation():
    """
    Daily job to rotate challenges.
    - Deactivates all challenges
    - Activates today's challenge
    
    Runs at 00:00 UTC every day.
    """
    logger.info(f"Running daily challenge rotation at {datetime.utcnow()}")
    
    async with AsyncSessionLocal() as db:
        try:
            challenge = await activate_today_challenge(db)
            if challenge:
                logger.info(f"Activated challenge: {challenge.title}")
            else:
                logger.warning("No challenge found for today")
        except Exception as e:
            logger.error(f"Error in daily challenge rotation: {e}")
            await db.rollback()


def start_scheduler():
    """Start the background scheduler."""
    # Add daily challenge rotation job - runs at midnight UTC
    scheduler.add_job(
        daily_challenge_rotation,
        CronTrigger(hour=0, minute=0, timezone="UTC"),
        id="daily_challenge_rotation",
        name="Daily Challenge Rotation",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started successfully")


def stop_scheduler():
    """Stop the background scheduler."""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
