"""Caido Proxy Integration for xnLinkFinder-Z."""
from typing import List, Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class CaidoIntegration:
    """Integrate with Caido proxy."""
    
    def __init__(self, api_url: str = "http://localhost:8080", api_token: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token
        self.headers = {'Authorization': f'Bearer {api_token}'} if api_token else {}
    
    def push_endpoints(self, endpoints: List[str]) -> bool:
        """Push endpoints to Caido."""
        try:
            response = requests.post(
                f"{self.api_url}/api/endpoints",
                json={'endpoints': endpoints},
                headers=self.headers
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pushing to Caido: {e}")
            return False

def push_to_caido(endpoints: List[str], api_url: str, api_token: Optional[str] = None) -> bool:
    """Convenience function to push endpoints to Caido."""
    integration = CaidoIntegration(api_url, api_token)
    return integration.push_endpoints(endpoints)
