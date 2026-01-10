"""
Shodan Integration for xnLinkFinder-Z.

Features:
- Query Shodan API for target information
- Pull open ports, services, technologies
- Historical data analysis
- Vulnerability correlation
"""

from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class ShodanIntegration:
    """Shodan API integration for host intelligence gathering."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Shodan integration.
        
        Args:
            api_key: Shodan API key (optional, can be set later)
        """
        self.api_key = api_key
        self.client = None
        self._initialized = False
    
    def _initialize_client(self):
        """Lazy-load Shodan client."""
        if self._initialized:
            return
        
        if not self.api_key:
            logger.warning("Shodan API key not provided")
            self._initialized = True
            return
        
        try:
            import shodan
            self.client = shodan.Shodan(self.api_key)
            self._initialized = True
            logger.info("Initialized Shodan client")
        except ImportError:
            logger.warning("shodan library not available, install with: pip install shodan")
            self._initialized = True
        except Exception as e:
            logger.error(f"Error initializing Shodan client: {e}")
            self._initialized = True
    
    def search_host(self, ip_address: str) -> Dict[str, Any]:
        """
        Get information about a specific host.
        
        Args:
            ip_address: Target IP address
            
        Returns:
            Dictionary with host information
        """
        if not self._initialized:
            self._initialize_client()
        
        if not self.client:
            return {
                'error': 'Shodan client not available',
                'ip': ip_address
            }
        
        try:
            host_info = self.client.host(ip_address)
            
            result = {
                'ip': ip_address,
                'hostnames': host_info.get('hostnames', []),
                'organization': host_info.get('org', 'Unknown'),
                'os': host_info.get('os', 'Unknown'),
                'ports': host_info.get('ports', []),
                'services': [],
                'vulnerabilities': [],
                'technologies': set(),
                'last_update': host_info.get('last_update', 'Unknown')
            }
            
            # Extract service information
            for service in host_info.get('data', []):
                service_info = {
                    'port': service.get('port'),
                    'protocol': service.get('transport', 'tcp'),
                    'product': service.get('product', ''),
                    'version': service.get('version', ''),
                    'banner': service.get('data', '')[:200]  # First 200 chars
                }
                result['services'].append(service_info)
                
                # Extract technologies
                if service.get('product'):
                    result['technologies'].add(service['product'])
            
            # Extract vulnerabilities
            for service in host_info.get('data', []):
                if 'vulns' in service:
                    for vuln in service['vulns']:
                        result['vulnerabilities'].append({
                            'cve': vuln,
                            'port': service.get('port')
                        })
            
            result['technologies'] = list(result['technologies'])
            
            return result
        
        except Exception as e:
            logger.error(f"Error querying Shodan for {ip_address}: {e}")
            return {
                'error': str(e),
                'ip': ip_address
            }
    
    def search_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Search for hosts related to a domain.
        
        Args:
            domain: Target domain
            
        Returns:
            List of host information dictionaries
        """
        if not self._initialized:
            self._initialize_client()
        
        if not self.client:
            return []
        
        try:
            results = self.client.search(f'hostname:{domain}')
            
            hosts = []
            for result in results['matches']:
                host = {
                    'ip': result.get('ip_str'),
                    'port': result.get('port'),
                    'organization': result.get('org', 'Unknown'),
                    'hostnames': result.get('hostnames', []),
                    'product': result.get('product', ''),
                    'version': result.get('version', ''),
                    'os': result.get('os', ''),
                }
                hosts.append(host)
            
            logger.info(f"Found {len(hosts)} hosts for domain {domain}")
            return hosts
        
        except Exception as e:
            logger.error(f"Error searching Shodan for domain {domain}: {e}")
            return []
    
    def search_query(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Execute a custom Shodan search query.
        
        Args:
            query: Shodan search query
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        if not self._initialized:
            self._initialize_client()
        
        if not self.client:
            return []
        
        try:
            results = self.client.search(query, limit=limit)
            
            matches = []
            for result in results['matches']:
                match = {
                    'ip': result.get('ip_str'),
                    'port': result.get('port'),
                    'organization': result.get('org', 'Unknown'),
                    'hostnames': result.get('hostnames', []),
                    'location': {
                        'country': result.get('location', {}).get('country_name'),
                        'city': result.get('location', {}).get('city'),
                    },
                    'data': result.get('data', '')[:500]  # First 500 chars
                }
                matches.append(match)
            
            logger.info(f"Found {len(matches)} results for query: {query}")
            return matches
        
        except Exception as e:
            logger.error(f"Error executing Shodan query '{query}': {e}")
            return []
    
    def get_ports_for_host(self, ip_address: str) -> List[int]:
        """
        Get list of open ports for a host.
        
        Args:
            ip_address: Target IP address
            
        Returns:
            List of open port numbers
        """
        host_info = self.search_host(ip_address)
        return host_info.get('ports', [])
    
    def get_vulnerabilities(self, ip_address: str) -> List[Dict[str, Any]]:
        """
        Get known vulnerabilities for a host.
        
        Args:
            ip_address: Target IP address
            
        Returns:
            List of vulnerability dictionaries
        """
        host_info = self.search_host(ip_address)
        return host_info.get('vulnerabilities', [])
    
    def analyze_target(self, target: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a target.
        
        Args:
            target: IP address or domain name
            
        Returns:
            Comprehensive analysis dictionary
        """
        import re
        
        # Determine if target is IP or domain
        is_ip = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target)
        
        if is_ip:
            # Direct host lookup
            return {
                'target': target,
                'type': 'ip',
                'host_info': self.search_host(target)
            }
        else:
            # Domain search
            hosts = self.search_domain(target)
            return {
                'target': target,
                'type': 'domain',
                'hosts_found': len(hosts),
                'hosts': hosts
            }


def search_shodan(target: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for Shodan searches.
    
    Args:
        target: IP address or domain to search
        api_key: Shodan API key
        
    Returns:
        Search results dictionary
    """
    integration = ShodanIntegration(api_key=api_key)
    return integration.analyze_target(target)
