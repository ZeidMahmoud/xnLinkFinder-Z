"""
Open Redirect Scanner

Detects open redirect vulnerabilities:
- Parameter-based redirects
- Path-based redirects
- Common bypass techniques
"""

import requests
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, parse_qs, urlencode
import re


class OpenRedirectScanner:
    """Scanner for open redirect vulnerabilities"""
    
    # Common redirect parameters
    REDIRECT_PARAMS = [
        'url', 'redirect', 'redirect_uri', 'redirect_url', 'return', 'return_to',
        'returnTo', 'return_url', 'next', 'goto', 'destination', 'dest', 'redir',
        'redirect_to', 'out', 'view', 'target', 'to', 'link', 'continue', 'go',
        'ref', 'referrer', 'forward', 'forward_url', 'callback', 'callback_url',
    ]
    
    # Test payloads
    PAYLOADS = [
        'https://evil.com',
        '//evil.com',
        '///evil.com',
        '////evil.com',
        'https:evil.com',
        'https://google.com',
        '//google.com',
        '/\\evil.com',
        '/\\/\\/evil.com',
        'javascript:alert(1)',
        '\x00//evil.com',
    ]
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize open redirect scanner
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def scan(self, url: str) -> List[Dict]:
        """
        Scan a URL for open redirect vulnerabilities
        
        Args:
            url: Target URL to scan
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        parsed = urlparse(url)
        
        # Get existing parameters
        params = parse_qs(parsed.query)
        
        # Test each redirect parameter
        for param in self.REDIRECT_PARAMS:
            vulns = self._test_parameter(url, param, params)
            vulnerabilities.extend(vulns)
            
        return vulnerabilities
    
    def _test_parameter(self, url: str, param: str, 
                       existing_params: Dict) -> List[Dict]:
        """Test a specific parameter for open redirect"""
        vulnerabilities = []
        
        for payload in self.PAYLOADS:
            try:
                # Build test URL
                test_params = existing_params.copy()
                test_params[param] = [payload]
                
                parsed = urlparse(url)
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if test_params:
                    test_url += '?' + urlencode(test_params, doseq=True)
                    
                # Make request without following redirects
                response = requests.get(
                    test_url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                # Check for redirect
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    
                    # Check if redirect points to our payload
                    if self._is_vulnerable_redirect(location, payload):
                        vulnerabilities.append({
                            'url': url,
                            'parameter': param,
                            'payload': payload,
                            'type': 'OPEN_REDIRECT',
                            'severity': 'MEDIUM',
                            'description': f'Open redirect via parameter {param}',
                            'redirect_location': location,
                            'status_code': response.status_code,
                        })
                        
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _is_vulnerable_redirect(self, location: str, payload: str) -> bool:
        """Check if redirect location indicates vulnerability"""
        if not location:
            return False
            
        location_lower = location.lower()
        payload_lower = payload.lower()
        
        # Check for exact match
        if payload_lower in location_lower:
            return True
            
        # Check for domain in redirect
        if 'evil.com' in location_lower or 'google.com' in location_lower:
            return True
            
        # Check for protocol-relative URL
        if location.startswith('//') and 'evil.com' in location_lower:
            return True
            
        # Check for JavaScript protocol
        if location.startswith('javascript:'):
            return True
            
        return False
    
    def test_path_based(self, url: str) -> List[Dict]:
        """
        Test for path-based open redirects
        
        Args:
            url: Base URL to test
            
        Returns:
            List of vulnerabilities
        """
        vulnerabilities = []
        
        # Path-based payloads
        path_payloads = [
            '/redirect/https://evil.com',
            '/goto/https://evil.com',
            '/.//evil.com',
            '/./https://evil.com',
        ]
        
        for payload in path_payloads:
            try:
                test_url = url.rstrip('/') + payload
                
                response = requests.get(
                    test_url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    
                    if 'evil.com' in location.lower():
                        vulnerabilities.append({
                            'url': test_url,
                            'type': 'OPEN_REDIRECT_PATH',
                            'severity': 'MEDIUM',
                            'description': 'Path-based open redirect',
                            'redirect_location': location,
                        })
                        
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def extract_redirect_params(self, url: str) -> Set[str]:
        """
        Extract potential redirect parameters from URL
        
        Args:
            url: URL to analyze
            
        Returns:
            Set of potential redirect parameters
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        found_params = set()
        
        for param in params.keys():
            param_lower = param.lower()
            if any(redir in param_lower for redir in 
                   ['redirect', 'return', 'url', 'goto', 'next', 'forward']):
                found_params.add(param)
                
        return found_params


def scan_open_redirects(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """
    Convenience function to scan multiple URLs
    
    Args:
        urls: List of URLs to scan
        **kwargs: Additional arguments for OpenRedirectScanner
        
    Returns:
        Dictionary mapping URLs to vulnerabilities
    """
    scanner = OpenRedirectScanner(**kwargs)
    results = {}
    
    for url in urls:
        try:
            vulns = scanner.scan(url)
            path_vulns = scanner.test_path_based(url)
            
            all_vulns = vulns + path_vulns
            if all_vulns:
                results[url] = all_vulns
                
        except Exception as e:
            print(f"[!] Error scanning {url}: {str(e)}")
            
    return results
