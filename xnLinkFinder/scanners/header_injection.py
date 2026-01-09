"""
Header Injection Scanner

Detects header injection vulnerabilities:
- CRLF injection
- Host header injection
- X-Forwarded-* header abuse
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse
import re


class HeaderInjectionScanner:
    """Scanner for header injection vulnerabilities"""
    
    # CRLF injection payloads
    CRLF_PAYLOADS = [
        '\r\nInjected-Header: test',
        '\rInjected-Header: test',
        '\nInjected-Header: test',
        '%0d%0aInjected-Header: test',
        '%0dInjected-Header: test',
        '%0aInjected-Header: test',
        '\r\n\r\nHTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>Injected</html>',
    ]
    
    # Host header bypass values
    HOST_PAYLOADS = [
        'evil.com',
        'localhost',
        '127.0.0.1',
        'attacker.com',
    ]
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize header injection scanner
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def scan(self, url: str) -> List[Dict]:
        """
        Scan for header injection vulnerabilities
        
        Args:
            url: Target URL to scan
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        # Test CRLF injection
        crlf_vulns = self._test_crlf_injection(url)
        vulnerabilities.extend(crlf_vulns)
        
        # Test Host header injection
        host_vulns = self._test_host_header(url)
        vulnerabilities.extend(host_vulns)
        
        # Test X-Forwarded headers
        xff_vulns = self._test_xff_headers(url)
        vulnerabilities.extend(xff_vulns)
        
        return vulnerabilities
    
    def _test_crlf_injection(self, url: str) -> List[Dict]:
        """Test for CRLF injection in URL parameters"""
        vulnerabilities = []
        parsed = urlparse(url)
        
        # Test in URL path
        for payload in self.CRLF_PAYLOADS:
            try:
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}{payload}"
                
                response = requests.get(
                    test_url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                # Check if injected header appears in response
                if self._check_crlf_injection(response, payload):
                    vulnerabilities.append({
                        'url': url,
                        'type': 'CRLF_INJECTION',
                        'severity': 'HIGH',
                        'description': 'CRLF injection in URL',
                        'payload': payload,
                        'injected_header': self._extract_injected_header(payload),
                    })
                    
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _test_host_header(self, url: str) -> List[Dict]:
        """Test for Host header injection"""
        vulnerabilities = []
        parsed = urlparse(url)
        
        for payload in self.HOST_PAYLOADS:
            try:
                # Try to inject Host header
                response = requests.get(
                    url,
                    headers={'Host': payload},
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                # Check if injected host appears in response
                if payload in response.text:
                    # Check in common locations
                    vuln_locations = []
                    
                    # Check Location header
                    location = response.headers.get('Location', '')
                    if payload in location:
                        vuln_locations.append('Location header')
                        
                    # Check response body
                    if payload in response.text:
                        vuln_locations.append('response body')
                        
                    if vuln_locations:
                        vulnerabilities.append({
                            'url': url,
                            'type': 'HOST_HEADER_INJECTION',
                            'severity': 'MEDIUM',
                            'description': f'Host header injection reflected in {", ".join(vuln_locations)}',
                            'injected_host': payload,
                        })
                        
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _test_xff_headers(self, url: str) -> List[Dict]:
        """Test X-Forwarded-* header abuse"""
        vulnerabilities = []
        
        xff_headers = {
            'X-Forwarded-For': '127.0.0.1',
            'X-Forwarded-Host': 'evil.com',
            'X-Forwarded-Proto': 'https',
            'X-Original-URL': '/admin',
            'X-Rewrite-URL': '/admin',
        }
        
        for header_name, header_value in xff_headers.items():
            try:
                response = requests.get(
                    url,
                    headers={header_name: header_value},
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                # Check if header value appears in response
                if header_value in response.text or header_value in str(response.headers):
                    vulnerabilities.append({
                        'url': url,
                        'type': 'XFF_HEADER_ABUSE',
                        'severity': 'LOW',
                        'description': f'{header_name} header reflected in response',
                        'header': header_name,
                        'value': header_value,
                    })
                    
                # Check for bypass (different status code)
                # Make baseline request
                baseline = requests.get(
                    url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=False
                )
                
                if response.status_code != baseline.status_code:
                    vulnerabilities.append({
                        'url': url,
                        'type': 'XFF_HEADER_BYPASS',
                        'severity': 'MEDIUM',
                        'description': f'{header_name} header changes response',
                        'header': header_name,
                        'baseline_code': baseline.status_code,
                        'modified_code': response.status_code,
                    })
                    
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _check_crlf_injection(self, response, payload: str) -> bool:
        """Check if CRLF injection was successful"""
        # Check if injected header appears in raw response
        try:
            raw_headers = str(response.raw.headers)
            if 'Injected-Header' in raw_headers:
                return True
        except:
            pass
            
        # Check response headers
        if 'Injected-Header' in response.headers:
            return True
            
        return False
    
    def _extract_injected_header(self, payload: str) -> str:
        """Extract the header name from payload"""
        match = re.search(r'(Injected-Header|HTTP/)', payload)
        if match:
            return match.group(1)
        return 'unknown'


def scan_header_injection(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """
    Convenience function to scan multiple URLs
    
    Args:
        urls: List of URLs to scan
        **kwargs: Additional arguments for HeaderInjectionScanner
        
    Returns:
        Dictionary mapping URLs to vulnerabilities
    """
    scanner = HeaderInjectionScanner(**kwargs)
    results = {}
    
    for url in urls:
        try:
            vulns = scanner.scan(url)
            if vulns:
                results[url] = vulns
        except Exception as e:
            print(f"[!] Error scanning {url}: {str(e)}")
            
    return results
