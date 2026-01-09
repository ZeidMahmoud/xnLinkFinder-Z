"""Certificate Transparency log mining."""
from typing import List
import requests
import logging

logger = logging.getLogger(__name__)

class CTLogMiner:
    """Mine subdomains and endpoints from CT logs."""
    
    def __init__(self):
        self.ct_api = "https://crt.sh"
    
    def discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains from CT logs."""
        subdomains = set()
        try:
            params = {'q': f'%.{domain}', 'output': 'json'}
            response = requests.get(self.ct_api, params=params, timeout=30)
            if response.status_code == 200:
                for entry in response.json():
                    name = entry.get('name_value', '')
                    if name:
                        subdomains.update(name.split('\n'))
        except Exception as e:
            logger.error(f"CT log mining failed: {e}")
        return list(subdomains)

def discover_ct_subdomains(domain: str) -> List[str]:
    """Convenience function for CT log subdomain discovery."""
    miner = CTLogMiner()
    return miner.discover_subdomains(domain)
