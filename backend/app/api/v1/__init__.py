"""
API v1 router configuration
"""
from fastapi import APIRouter
from app.api.v1.endpoints import projects, analysis, ai, analysis_enhanced

# Create API v1 router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)

api_router.include_router(
    analysis.router,
    prefix="/projects",
    tags=["analysis"]
)

api_router.include_router(
    analysis_enhanced.router,
    prefix="/projects",
    tags=["analysis-enhanced"]
)

api_router.include_router(
    ai.router,
    prefix="/ai",
    tags=["ai"]
)

# Made with Bob
