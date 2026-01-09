"""Wayback Machine integration for endpoint discovery."""
from typing import List, Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class WaybackMiner:
    """Mine historical endpoints from Wayback Machine."""
    
    def __init__(self, limit: int = 1000):
        self.limit = limit
        self.cdx_api = "http://web.archive.org/cdx/search/cdx"
    
    def discover_endpoints(self, domain: str) -> List[str]:
        """Discover historical endpoints for a domain."""
        try:
            params = {
                'url': f'{domain}/*',
                'output': 'json',
                'fl': 'original',
                'collapse': 'urlkey',
                'limit': self.limit
            }
            response = requests.get(self.cdx_api, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return [item[0] for item in data[1:] if item]  # Skip header
        except Exception as e:
            logger.error(f"Wayback discovery failed: {e}")
        return []

def discover_wayback_endpoints(domain: str, limit: int = 1000) -> List[str]:
    """Convenience function for Wayback endpoint discovery."""
    miner = WaybackMiner(limit)
    return miner.discover_endpoints(domain)
