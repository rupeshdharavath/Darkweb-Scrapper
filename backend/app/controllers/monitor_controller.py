"""Monitor controllers."""

from fastapi import HTTPException

from app.schemas.monitor import MonitorCreateRequest
from app.services.monitor_service import MonitorService


async def list_monitors_controller():
    """Return all monitors."""
    try:
        return await MonitorService.list_monitors()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def create_monitor_controller(request: MonitorCreateRequest):
    """Create a monitor."""
    try:
        return await MonitorService.create_monitor(request.url, request.interval)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def get_monitor_controller(monitor_id: str):
    """Return monitor by id."""
    try:
        return await MonitorService.get_monitor(monitor_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def delete_monitor_controller(monitor_id: str):
    """Delete monitor by id."""
    try:
        return await MonitorService.delete_monitor(monitor_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def delete_all_monitors_controller():
    """Delete all monitors."""
    try:
        return await MonitorService.delete_all_monitors()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def pause_monitor_controller(monitor_id: str):
    """Pause monitor."""
    try:
        return await MonitorService.pause_monitor(monitor_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to pause monitor")


async def resume_monitor_controller(monitor_id: str):
    """Resume monitor."""
    try:
        return await MonitorService.resume_monitor(monitor_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to resume monitor")
