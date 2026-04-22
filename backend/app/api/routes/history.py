"""
History-related API routes
"""

from fastapi import APIRouter
from app.schemas.history import HistoryListResponse, HistoryDetailResponse
from app.controllers.history_controller import (
    get_history_controller,
    get_history_entry_controller,
)

router = APIRouter()


@router.get("/history", response_model=HistoryListResponse, tags=["History"])
async def get_history():
    """
    Get all scan history sorted by newest first
    """
    return await get_history_controller()


@router.get("/history/{entry_id}", response_model=HistoryDetailResponse, tags=["History"])
async def get_history_entry(entry_id: str):
    """
    Get specific scan entry by ID
    
    - **entry_id**: MongoDB ObjectId of the scan entry
    """
    return await get_history_entry_controller(entry_id)
