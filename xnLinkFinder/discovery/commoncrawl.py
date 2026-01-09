"""CommonCrawl integration for endpoint discovery."""
from typing import List, Dict
import requests
import logging

logger = logging.getLogger(__name__)

class CommonCrawlMiner:
    """Mine endpoints from CommonCrawl index."""
    
    def __init__(self):
        self.index_api = "https://index.commoncrawl.org"
    
    def discover_endpoints(self, domain: str) -> List[str]:
        """Discover endpoints from CommonCrawl."""
        endpoints = []
        try:
            url = f"{self.index_api}/CC-MAIN-2023-50-index"
            params = {'url': f'*.{domain}/*', 'output': 'json'}
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.strip():
                        import json
                        data = json.loads(line)
                        endpoints.append(data.get('url', ''))
        except Exception as e:
            logger.error(f"CommonCrawl discovery failed: {e}")
        return endpoints

def discover_commoncrawl_endpoints(domain: str) -> List[str]:
    """Convenience function for CommonCrawl discovery."""
    miner = CommonCrawlMiner()
    return miner.discover_endpoints(domain)
