"""
Monitor management API routes
"""

from fastapi import APIRouter
from app.schemas.monitor import (
    MonitorCreateRequest,
    MonitorCreateResponse,
    MonitorListResponse,
    MonitorResponse,
    MonitorDeleteResponse,
    MonitorDeleteAllResponse,
    MonitorActionResponse
)
from app.controllers.monitor_controller import (
    list_monitors_controller,
    create_monitor_controller,
    get_monitor_controller,
    delete_monitor_controller,
    delete_all_monitors_controller,
    pause_monitor_controller,
    resume_monitor_controller,
)

router = APIRouter()


@router.get("/monitors", response_model=MonitorListResponse, tags=["Monitors"])
async def list_monitors():
    """
    Get all active monitors with last scan details
    """
    return await list_monitors_controller()


@router.post("/monitors", response_model=MonitorCreateResponse, status_code=201, tags=["Monitors"])
async def create_monitor(request: MonitorCreateRequest):
    """
    Create a new monitoring job
    
    - **url**: URL to monitor
    - **interval**: Monitoring interval in minutes (default: 5)
    """
    return await create_monitor_controller(request)


@router.get("/monitors/{monitor_id}", response_model=MonitorResponse, tags=["Monitors"])
async def get_monitor(monitor_id: str):
    """
    Get specific monitor details
    
    - **monitor_id**: Unique monitor identifier
    """
    return await get_monitor_controller(monitor_id)


@router.delete("/monitors/all", response_model=MonitorDeleteAllResponse, tags=["Monitors"])
async def delete_all_monitors():
    """
    Delete all monitors (utility endpoint)
    """
    return await delete_all_monitors_controller()


@router.delete("/monitors/{monitor_id}", response_model=MonitorDeleteResponse, tags=["Monitors"])
async def delete_monitor(monitor_id: str):
    """
    Delete a specific monitor

    - **monitor_id**: Unique monitor identifier
    """
    return await delete_monitor_controller(monitor_id)


@router.post("/monitors/{monitor_id}/pause", response_model=MonitorActionResponse, tags=["Monitors"])
async def pause_monitor(monitor_id: str):
    """
    Pause a monitor
    
    - **monitor_id**: Unique monitor identifier
    """
    return await pause_monitor_controller(monitor_id)


@router.post("/monitors/{monitor_id}/resume", response_model=MonitorActionResponse, tags=["Monitors"])
async def resume_monitor(monitor_id: str):
    """
    Resume a paused monitor
    
    - **monitor_id**: Unique monitor identifier
    """
    return await resume_monitor_controller(monitor_id)
