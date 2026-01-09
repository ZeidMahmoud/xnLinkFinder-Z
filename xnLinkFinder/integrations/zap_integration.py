"""OWASP ZAP Integration for xnLinkFinder-Z."""
from typing import List, Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class ZAPIntegration:
    """Integrate with OWASP ZAP."""
    
    def __init__(self, api_url: str = "http://localhost:8080", api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
    
    def push_endpoints(self, endpoints: List[str]) -> bool:
        """Push endpoints to ZAP for scanning."""
        try:
            for endpoint in endpoints:
                params = {'apikey': self.api_key, 'url': endpoint}
                response = requests.get(f"{self.api_url}/JSON/spider/action/scan/", params=params)
            return True
        except Exception as e:
            logger.error(f"Error pushing to ZAP: {e}")
            return False

def push_to_zap(endpoints: List[str], api_url: str, api_key: Optional[str] = None) -> bool:
    """Convenience function to push endpoints to ZAP."""
    integration = ZAPIntegration(api_url, api_key)
    return integration.push_endpoints(endpoints)
