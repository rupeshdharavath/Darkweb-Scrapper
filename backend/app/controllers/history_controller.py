"""History controllers."""

from fastapi import HTTPException

from app.services.history_service import HistoryService


async def get_history_controller():
    """Return history list."""
    try:
        return await HistoryService.get_history()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}")


async def get_history_entry_controller(entry_id: str):
    """Return one history entry by id."""
    try:
        return await HistoryService.get_history_entry(entry_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}")
