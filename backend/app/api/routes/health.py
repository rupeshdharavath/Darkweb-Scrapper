"""
Health check endpoint
"""

from fastapi import APIRouter
from app.schemas.common import HealthResponse
from app.controllers.health_controller import health_check

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check_route():
    """
    Health check endpoint to verify API status
    """
    return await health_check()
