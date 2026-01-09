"""Python SDK Client"""
from typing import List, Dict, Optional
import requests

class XnLinkFinderClient:
    """Python SDK for xnLinkFinder API"""
    
    def __init__(self, base_url: str = "http://localhost:8080", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def scan(self, url: str, **kwargs) -> Dict:
        """Start a scan"""
        return self.session.post(f"{self.base_url}/scan", json={"url": url, **kwargs}).json()
    
    def get_results(self, scan_id: str) -> Dict:
        """Get scan results"""
        return self.session.get(f"{self.base_url}/scan/{scan_id}").json()
    
    async def scan_async(self, url: str, **kwargs) -> Dict:
        """Async scan"""
        return self.scan(url, **kwargs)
