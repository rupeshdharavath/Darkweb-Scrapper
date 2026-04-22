"""
Alert management API routes
"""

from fastapi import APIRouter
from app.schemas.alert import AlertListResponse, AcknowledgeResponse
from app.controllers.alert_controller import (
    get_alerts_controller,
    acknowledge_alert_controller,
)

router = APIRouter()


@router.get("/alerts", response_model=AlertListResponse, tags=["Alerts"])
async def get_alerts():
    """
    Get recent alerts (last 100)
    """
    return await get_alerts_controller()


@router.post("/alerts/{alert_id}/acknowledge", response_model=AcknowledgeResponse, tags=["Alerts"])
async def acknowledge_alert(alert_id: str):
    """
    Mark an alert as acknowledged
    
    - **alert_id**: MongoDB ObjectId of the alert
    """
    return await acknowledge_alert_controller(alert_id)
