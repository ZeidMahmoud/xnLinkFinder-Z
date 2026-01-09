"""
CORS Misconfiguration Scanner

Detects insecure CORS configurations including:
- Credential leakage via CORS
- Wildcard origin issues
- Null origin acceptance
- Reflected origins
"""

import requests
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


class CORSScanner:
    """Scanner for detecting CORS misconfigurations"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize CORS scanner
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.test_origins = [
            "https://evil.com",
            "null",
            "https://attacker.com",
        ]
        
    def scan(self, url: str, cookies: Optional[Dict] = None, 
             headers: Optional[Dict] = None) -> List[Dict]:
        """
        Scan a URL for CORS misconfigurations
        
        Args:
            url: Target URL to scan
            cookies: Optional cookies to include
            headers: Optional headers to include
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        for origin in self.test_origins:
            try:
                vuln = self._test_origin(url, origin, cookies, headers)
                if vuln:
                    vulnerabilities.append(vuln)
            except Exception as e:
                print(f"[!] Error testing origin {origin}: {str(e)}")
                
        # Test for reflected origin
        try:
            reflected = self._test_reflected_origin(url, cookies, headers)
            if reflected:
                vulnerabilities.append(reflected)
        except Exception as e:
            print(f"[!] Error testing reflected origin: {str(e)}")
            
        return vulnerabilities
    
    def _test_origin(self, url: str, origin: str, 
                     cookies: Optional[Dict], 
                     headers: Optional[Dict]) -> Optional[Dict]:
        """Test a specific origin for CORS misconfiguration"""
        test_headers = headers.copy() if headers else {}
        test_headers['Origin'] = origin
        
        try:
            response = requests.get(
                url,
                headers=test_headers,
                cookies=cookies,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=False
            )
            
            acao = response.headers.get('Access-Control-Allow-Origin', '')
            acac = response.headers.get('Access-Control-Allow-Credentials', '')
            
            # Check for vulnerable configuration
            if acao == origin and acac.lower() == 'true':
                return {
                    'url': url,
                    'type': 'CORS_CREDENTIALS_LEAK',
                    'severity': 'HIGH',
                    'description': f'CORS allows credentials with origin: {origin}',
                    'acao': acao,
                    'acac': acac,
                }
            elif acao == '*' and acac.lower() == 'true':
                return {
                    'url': url,
                    'type': 'CORS_WILDCARD_WITH_CREDENTIALS',
                    'severity': 'HIGH',
                    'description': 'CORS allows wildcard origin with credentials',
                    'acao': acao,
                    'acac': acac,
                }
            elif acao == origin:
                return {
                    'url': url,
                    'type': 'CORS_PERMISSIVE',
                    'severity': 'MEDIUM',
                    'description': f'CORS allows origin: {origin}',
                    'acao': acao,
                }
                
        except requests.RequestException:
            pass
            
        return None
    
    def _test_reflected_origin(self, url: str, 
                               cookies: Optional[Dict],
                               headers: Optional[Dict]) -> Optional[Dict]:
        """Test for reflected origin vulnerability"""
        test_origin = f"https://{urlparse(url).netloc}.evil.com"
        test_headers = headers.copy() if headers else {}
        test_headers['Origin'] = test_origin
        
        try:
            response = requests.get(
                url,
                headers=test_headers,
                cookies=cookies,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=False
            )
            
            acao = response.headers.get('Access-Control-Allow-Origin', '')
            acac = response.headers.get('Access-Control-Allow-Credentials', '')
            
            if test_origin in acao:
                return {
                    'url': url,
                    'type': 'CORS_REFLECTED_ORIGIN',
                    'severity': 'HIGH' if acac.lower() == 'true' else 'MEDIUM',
                    'description': 'CORS reflects arbitrary origin',
                    'tested_origin': test_origin,
                    'acao': acao,
                    'acac': acac,
                }
                
        except requests.RequestException:
            pass
            
        return None


def scan_cors(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """
    Convenience function to scan multiple URLs
    
    Args:
        urls: List of URLs to scan
        **kwargs: Additional arguments for CORSScanner
        
    Returns:
        Dictionary mapping URLs to vulnerabilities
    """
    scanner = CORSScanner(**kwargs)
    results = {}
    
    for url in urls:
        try:
            vulns = scanner.scan(url)
            if vulns:
                results[url] = vulns
        except Exception as e:
            print(f"[!] Error scanning {url}: {str(e)}")
            
    return results
