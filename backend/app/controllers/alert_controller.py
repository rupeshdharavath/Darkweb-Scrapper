"""Alert controllers."""

from fastapi import HTTPException

from app.services.alert_service import AlertService


async def get_alerts_controller():
    """Return latest alerts."""
    try:
        return await AlertService.get_alerts()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}")


async def acknowledge_alert_controller(alert_id: str):
    """Acknowledge one alert by id."""
    try:
        return await AlertService.acknowledge_alert(alert_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")
