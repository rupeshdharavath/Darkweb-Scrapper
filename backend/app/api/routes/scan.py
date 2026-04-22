"""
Scan-related API routes
"""

from fastapi import APIRouter
from app.schemas.scan import ScanRequest, ScanResponse
from app.schemas.common import ComparisonResponse
from app.controllers.scan_controller import scan_url_controller, compare_scans_controller

router = APIRouter()


@router.post("/scan", response_model=ScanResponse, tags=["Scan"])
async def scan_url(request: ScanRequest):
    """
    Scan a URL and return threat analysis
    
    - **url**: URL to scan (must include http:// or https://)
    """
    return await scan_url_controller(request)


@router.get("/compare", response_model=ComparisonResponse, tags=["Scan"])
async def compare_scans(url: str):
    """
    Compare current scan with baseline (first) scan for a URL
    
    - **url**: URL to compare scans for
    """
    return await compare_scans_controller(url)
