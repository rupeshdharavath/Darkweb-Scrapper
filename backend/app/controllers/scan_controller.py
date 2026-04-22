"""Scan controllers."""

from fastapi import HTTPException

from app.schemas.scan import ScanRequest
from app.services.scan_service import ScanService


async def scan_url_controller(request: ScanRequest):
    """Handle scan request."""
    try:
        return await ScanService.scan_url(request.url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


async def compare_scans_controller(url: str):
    """Handle scan comparison request."""
    try:
        return await ScanService.compare_scans(url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")
