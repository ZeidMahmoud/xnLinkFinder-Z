"""API Routes"""
from typing import Dict

def register_routes(app):
    """Register all API routes"""
    pass

def get_scan_status(scan_id: str) -> Dict:
    return {"scan_id": scan_id, "status": "unknown"}
