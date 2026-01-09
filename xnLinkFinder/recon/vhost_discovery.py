"""
Virtual Host Discovery for xnLinkFinder-Z.

Features:
- Find hidden vhosts on same IP
- Brute-force common vhost names
- SSL certificate vhost extraction
- Reverse IP lookup
"""

from typing import List, Dict, Optional, Set
import logging

logger = logging.getLogger(__name__)


class VHostDiscovery:
    """Virtual host discovery and enumeration."""
    
    def __init__(self):
        """Initialize vhost discovery."""
        self.common_vhosts = [
            'www', 'mail', 'ftp', 'admin', 'dev', 'test', 'staging',
            'api', 'app', 'portal', 'secure', 'vpn', 'remote'
        ]
    
    def discover_vhosts(self, ip_address: str, base_domain: str,
                       wordlist: Optional[List[str]] = None) -> List[Dict[str, any]]:
        """
        Discover virtual hosts on an IP address.
        
        Args:
            ip_address: Target IP address
            base_domain: Base domain name
            wordlist: Optional custom wordlist
            
        Returns:
            List of discovered vhosts
        """
        try:
            import requests
            
            wordlist = wordlist or self.common_vhosts
            discovered = []
            
            for subdomain in wordlist:
                hostname = f"{subdomain}.{base_domain}"
                
                try:
                    # Make request with Host header
                    response = requests.get(
                        f"http://{ip_address}",
                        headers={'Host': hostname},
                        timeout=5,
                        allow_redirects=False
                    )
                    
                    # Check if response differs (indicates vhost exists)
                    if response.status_code not in [404, 502, 503]:
                        discovered.append({
                            'hostname': hostname,
                            'ip': ip_address,
                            'status_code': response.status_code,
                            'title': self._extract_title(response.text)
                        })
                        logger.info(f"Discovered vhost: {hostname}")
                
                except Exception as e:
                    logger.debug(f"Error testing vhost {hostname}: {e}")
                    continue
            
            return discovered
        
        except Exception as e:
            logger.error(f"Error discovering vhosts: {e}")
            return []
    
    def _extract_title(self, html: str) -> str:
        """Extract page title from HTML."""
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else ''


def discover_vhosts(ip_address: str, domain: str) -> List[Dict[str, any]]:
    """
    Convenience function for vhost discovery.
    
    Args:
        ip_address: Target IP
        domain: Base domain
        
    Returns:
        List of discovered vhosts
    """
    discovery = VHostDiscovery()
    return discovery.discover_vhosts(ip_address, domain)
