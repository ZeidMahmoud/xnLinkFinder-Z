"""Tor/Proxy rotation for stealth scanning."""
from typing import List, Optional
import logging
import random

logger = logging.getLogger(__name__)

class ProxyRotator:
    """Rotate proxies for stealth scanning."""
    
    def __init__(self, proxy_list: Optional[List[str]] = None, use_tor: bool = False):
        self.proxy_list = proxy_list or []
        self.use_tor = use_tor
        self.current_index = 0
    
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy in rotation."""
        if self.use_tor:
            return {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
        elif self.proxy_list:
            proxy = self.proxy_list[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxy_list)
            return {'http': proxy, 'https': proxy}
        return None
    
    def load_proxies_from_file(self, filepath: str):
        """Load proxy list from file."""
        try:
            with open(filepath, 'r') as f:
                self.proxy_list = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Failed to load proxies: {e}")
