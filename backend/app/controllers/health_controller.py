"""Health controller."""


async def health_check():
    """Return API health status."""
    return {"status": "ok"}
