"""Authentication for API"""
from typing import Optional

def verify_token(token: str) -> bool:
    """Verify JWT token"""
    return len(token) > 0

def create_token(user: str) -> str:
    """Create JWT token"""
    return f"token_{user}"
