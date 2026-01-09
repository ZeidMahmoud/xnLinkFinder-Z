"""Search engine integration (Shodan/Censys/Fofa)."""
from typing import List, Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class ShodanSearch:
    """Search Shodan for exposed services."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.shodan.io"
    
    def search(self, query: str) -> List[Dict]:
        """Search Shodan."""
        try:
            params = {'key': self.api_key, 'query': query}
            response = requests.get(f"{self.api_url}/shodan/host/search", params=params)
            if response.status_code == 200:
                return response.json().get('matches', [])
        except Exception as e:
            logger.error(f"Shodan search failed: {e}")
        return []

def search_shodan(domain: str, api_key: str) -> List[Dict]:
    """Search Shodan for a domain."""
    searcher = ShodanSearch(api_key)
    return searcher.search(f'hostname:{domain}')
