"""
Censys Integration for xnLinkFinder-Z.

Features:
- Certificate search
- Host enumeration
- Protocol detection
"""

from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class CensysIntegration:
    """Censys API integration for certificate and host intelligence."""
    
    def __init__(self, api_id: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Censys integration.
        
        Args:
            api_id: Censys API ID
            api_secret: Censys API secret
        """
        self.api_id = api_id
        self.api_secret = api_secret
        self.client = None
        self._initialized = False
    
    def _initialize_client(self):
        """Lazy-load Censys client."""
        if self._initialized:
            return
        
        if not self.api_id or not self.api_secret:
            logger.warning("Censys API credentials not provided")
            self._initialized = True
            return
        
        try:
            from censys.search import CensysCertificates, CensysHosts
            self.certs_client = CensysCertificates(self.api_id, self.api_secret)
            self.hosts_client = CensysHosts(self.api_id, self.api_secret)
            self._initialized = True
            logger.info("Initialized Censys client")
        except ImportError:
            logger.warning("censys library not available, install with: pip install censys")
            self._initialized = True
        except Exception as e:
            logger.error(f"Error initializing Censys client: {e}")
            self._initialized = True
    
    def search_certificates(self, domain: str) -> List[Dict[str, Any]]:
        """
        Search for certificates related to a domain.
        
        Args:
            domain: Target domain
            
        Returns:
            List of certificate information
        """
        if not self._initialized:
            self._initialize_client()
        
        if not self.certs_client:
            return []
        
        try:
            query = f"parsed.names: {domain}"
            results = []
            
            for cert in self.certs_client.search(query, max_records=100):
                results.append({
                    'fingerprint': cert.get('fingerprint_sha256'),
                    'names': cert.get('parsed', {}).get('names', []),
                    'issuer': cert.get('parsed', {}).get('issuer', {}),
                    'validity': cert.get('parsed', {}).get('validity', {})
                })
            
            logger.info(f"Found {len(results)} certificates for {domain}")
            return results
        
        except Exception as e:
            logger.error(f"Error searching Censys certificates for {domain}: {e}")
            return []
    
    def search_hosts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for hosts.
        
        Args:
            query: Censys search query
            
        Returns:
            List of host information
        """
        if not self._initialized:
            self._initialize_client()
        
        if not self.hosts_client:
            return []
        
        try:
            results = []
            
            for host in self.hosts_client.search(query, max_records=100):
                results.append({
                    'ip': host.get('ip'),
                    'services': host.get('services', []),
                    'location': host.get('location', {}),
                    'autonomous_system': host.get('autonomous_system', {})
                })
            
            logger.info(f"Found {len(results)} hosts")
            return results
        
        except Exception as e:
            logger.error(f"Error searching Censys hosts: {e}")
            return []


def search_censys(domain: str, api_id: Optional[str] = None, 
                  api_secret: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for Censys searches.
    
    Args:
        domain: Domain to search
        api_id: Censys API ID
        api_secret: Censys API secret
        
    Returns:
        Search results
    """
    integration = CensysIntegration(api_id=api_id, api_secret=api_secret)
    return {
        'domain': domain,
        'certificates': integration.search_certificates(domain)
    }
