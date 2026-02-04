"""
Daily Challenge App - FastAPI Backend
Main application entry point.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers import auth_router, challenge_router, user_router
from app.services.scheduler import start_scheduler, stop_scheduler
from app.services.challenge import activate_today_challenge
from app.database import AsyncSessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Daily Challenge App...")
    
    # Create database tables
    await create_tables()
    logger.info("Database tables created")
    
    # Activate today's challenge
    async with AsyncSessionLocal() as db:
        await activate_today_challenge(db)
    logger.info("Today's challenge activated")
    
    # Start scheduler for daily jobs
    start_scheduler()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Daily Challenge App...")
    stop_scheduler()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="A brutalist daily challenge application. One challenge per day. No excuses.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS - uses settings for production flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False if "*" in settings.cors_origins_list else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(challenge_router)
app.include_router(user_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "DAILY CHALLENGE",
        "tagline": "One challenge. Every day. No excuses.",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
